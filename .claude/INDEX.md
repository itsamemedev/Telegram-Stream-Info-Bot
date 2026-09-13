# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9379  GET              /                                                dashboard
 11292  GET              /api/abo/status                                  api_abo_status
 11246  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10167  GET              /api/automation/status                           api_automation_status
 10189  POST             /api/automation/toggle                           api_automation_toggle
 18401  GET              /api/channel/categories                          api_channel_categories
 18407  POST             /api/channel/set                                 api_channel_set
 18254  GET              /api/channels/status                             api_channels_status
 17928  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 17911  GET              /api/clips                                       api_clips
 17957  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17836  GET              /api/debug/threads                               api_debug_threads
 11257  GET              /api/events                                      api_events
 10808  GET              /api/events/stream                               api_events_stream
 10635  GET              /api/health                                      api_health
 17870  POST             /api/highlights/config                           api_highlights_config
  9313  POST             /api/login                                       dashboard_login_submit
 11582  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 10723  GET              /api/notify/status                               api_notify_status
 10734  POST             /api/notify/test                                 api_notify_test
 11346  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11323  GET              /api/proxy/trend                                 api_proxy_trend
 17977  GET              /api/tts/<fn>                                    api_tts_file
 18752  GET              /api/upload_window                               api_upload_window
 10925  GET              /archive/<int:eid>/download                      archive_download
 10953  GET              /download/<int:recording_id>                     download
 10882  GET              /health                                          health
 17805  GET              /healthz                                         healthz
  9304  GET              /login                                           dashboard_login_page
  9334  GET              /logout                                          dashboard_logout
  9341  GET              /manifest.webmanifest                            pwa_manifest
 18725  GET              /overlay                                         overlay_page
  9365  GET              /pwa-icon-<variant>.png                          pwa_icon
  9351  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (330)

```
   182  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   394  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
  1003  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   743  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   874  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   854  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   892  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   816  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   551  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   649  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1241  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1273  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   340  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   956  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   936  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1109  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1157  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1208  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1067  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   911  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   389  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   653  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   535  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   518  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   510  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   346  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   362  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   697  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   662  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   682  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   569  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   286  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   371  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   348  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   161  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   415  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   329  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   314  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   237  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   193  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    71  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    78  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   469  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   258  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   285  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   245  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   366  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   284  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   386  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   381  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   457  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   400  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   267  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   334  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   362  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   213  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   280  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   515  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   178  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   161  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   401  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   225  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   177  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   460  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   435  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   296  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   142  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   835  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   917  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   945  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   956  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   822  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   884  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   871  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   852  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   497  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   492  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   540  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   423  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   750  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   514  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   477  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   450  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   724  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   594  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   683  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   589  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   522  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   302  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   767  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   390  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   645  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   800  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   785  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   346  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   584  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   570  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   553  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   610  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1071  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1146  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1035  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   703  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   599  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   486  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   464  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   505  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   574  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   440  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   596  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   535  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   561  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   370  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   360  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   395  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   338  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   428  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   448  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   340  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   370  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   206  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    72  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   117  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   140  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   104  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   370  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   361  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   176  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   238  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   453  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   482  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   402  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   415  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   511  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   388  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   263  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   308  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   332  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   319  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   165  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   277  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   135  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   369  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   424  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   252  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   463  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   429  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   488  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   468  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   451  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   444  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   238  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   305  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   382  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (60)

```
   803  /ai                     
  1207  /ask                    
   904  /assign_role            
   954  /ban                    
  2065  /botstats               
  1466  /clearwarns             
  2029  /clip                   
  2014  /clipoftheweek          
  1333  /clips                  
   859  /create_category        
   830  /create_channel         
   894  /create_group           
   869  /create_role            
   845  /create_voice           
  1090  /daily                  
  1236  /event                  
  1278  /events                 
  1376  /follow                 
  1361  /help                   
   944  /kick                   
  1065  /leaderboard            
  1320  /livenow                
  1348  /post_test              
  1168  /profile                
   976  /purge                  
  1052  /rank                   
  1308  /recstatus              
   914  /remove_role            
   816  /restream_status        
   924  /set_channel_perms      
  1019  /setup_community        
  1036  /setup_targets          
  1408  /stats                  
   733  /status                 
  1537  /streaminfo             
  2117  /sys_aireset            KI-Kontext zurücksetzen (TG: /aireset)
  2119  /sys_bulkadd            Mehrere User tracken (TG: /bulkadd a b c)
  2110  /sys_cleanup            Alte Aufnahmen aufräumen (TG: /cleanup)
  2121  /sys_cookies            Cookie-Status (TG: /cookies)
  2116  /sys_diag               Vollständige Diagnose (TG: /diag)
  2120  /sys_live               Live-Check erzwingen (TG: /live @user)
  2115  /sys_logs               Letzte Fehler-Logs (TG: /logs)
  2107  /sys_pause              Tracking pausieren (TG: /pause @user)
  2111  /sys_quota              Speicher-Quota (TG: /quota)
  1521  /sys_report             
  2112  /sys_res                System-Ressourcen (TG: /sysres)
  2108  /sys_resume             Tracking fortsetzen (TG: /resume @user)
  2109  /sys_stoprec            Aufnahme grazil stoppen (TG: /stoprec @user)
  2114  /sys_summary            Tageszusammenfassung (TG: /summary)
  2118  /sys_teststream         Recorder-Selbsttest (TG: /teststream)
  2113  /sys_topusers           Top-Streamer-Statistik (TG: /topusers)
  1498  /sys_unpause            
   964  /timeout                
  1476  /topstreamers           
   761  /track                  
   746  /tracklist              
  1390  /unfollow               
   793  /untrack                
  1429  /warn                   
  1452  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2274  on_member_join
  2236  on_message
  2143  on_raw_reaction_add
  2309  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-456    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (45 Funktionen)

```
  1614-1665   _award_xp
  1834-1863   _clip_week_leader
  1887-1901   _clipoftheweek_loop
  2425-2487   _community_events_loop
  1571-1593   _dc_client
  1596-1605   _dc_offen
  2527-2562   _disc_automod_check
   423-428    _disc_sprache_setzen
  1668-1716   _discord_ai_automod
   556-595    _discord_automod
  1719-1739   _discord_azrael_reply
  1904-2384   _discord_run_once
   258-316    _discord_start
   319-373    _ensure_discord_invite
  2390-2422   _ensure_error_channel
   444-457    _ensure_rank_roles
   692-706    _ensure_team_roles
  2490-2520   _error_channel_loop
   605-609    _guard
   525-553    _handle_voice_ai
   431-441    _is_admin
  1782-1793   _liveboard_loop
   612-630    _on_level_up
   521-522    _par_chat_id
  1866-1884   _post_clip_of_week
  1796-1814   _post_weekly_digest
   460-486    _provision_base_channels
   489-505    _provision_user_channels
  1300-1397   _reg_betrieb
   990-1079   _reg_community_setup
  1082-1157   _reg_daily_profil
  1200-1297   _reg_frage_events
   720-818    _reg_info
   936-987    _reg_moderation
  1160-1197   _reg_profil
   885-933    _reg_rollen
   821-882    _reg_server
  1400-1487   _reg_streamer
  1490-1568   _reg_system
   665-689    _run_tg_handler
   508-518    _tracked_usernames
   163-237    _uebernehmen
  1748-1779   _update_liveboard
  1817-1831   _weekly_digest_loop
   240-243    starte
```

## Top-Level-Symbole in bot.py (497 Funktionen, 2 Klassen)

```
  2570-2571   _abo_key
  2591-2609   _abo_probe_dump
 14760-14767  _ad_allowlist
 15736-15742  _agent_for
 15745-15761  _ai_telemetry
 16256-16274  _alert
 19593-19643  _alert_monitor_loop
 19995-20057  _announce_loop
  3168-3178   _anthropic_key
  3185-3187   _anthropic_model
  9057-9060   _arg_int
  2562-2567   _as_dict
 22764-22773  _async_exc_handler
 16437-16459  _audio_tap_cmd
 16996-17055  _audio_tap_melden
 16473-16497  _audio_tap_sammler
  9225-9236   _auth_cookie
  9192-9221   _auth_guard
  1799-1804   _auto_on
 17667-17685  _auto_restream_loop
 12762-12804  _avatar_frames_laden
 21075-21090  _azrael_broadcast_reply
 20975-20997  _azrael_chat_reply
 20947-20972  _azrael_chat_should_reply
 21003-21005  _azrael_gate_cfg
 15766-15780  _azrael_live_state
 18638-18652  _azrael_overlay_state
 16138-16192  _azrael_proactive_loop
 15584-15640  _azrael_reaction_to_chats
 21008-21015  _azrael_reply_all_chats
 20934-20944  _azrael_self_names
 21043-21072  _azrael_send_to
 12723-12759  _azrael_spricht
 15786-15807  _azrael_system
 19727-19730  _backup_active
 19808-19821  _backup_loop
 22837-22846  _brain_crowdsec_snap
 19532-19541  _brain_growth_loop
  9558-9585   _brain_growth_snapshot
  2504-2524   _brain_hint_delay
 22909-22944  _brain_moderation_snap
  6007-6035   _brain_notify
 22947-22969  _brain_recording_snap
 22849-22906  _brain_restream_health
 22972-22985  _brain_tiktok_status_snap
 10787-10804  _browser_push
  6047-6134   _build_daily_summary
 13083-13087  _build_restream_cmd
  4829-4856   _can_stop_tracking
  1912-1934   _capture_set_cookies
 11400-11403  _cfg_get
 11406-11408  _cfg_set
 18362-18397  _channel_set_all
 11951-11954  _chat_connected
 11957-11973  _chat_disconnected
  8124-8135   _chat_is_forum
 16803-16828  _chat_listener_abbauen
 11993-11995  _chat_sanitize
 11936-11948  _chat_stat
 11976-11979  _chat_stats_snapshot
  3471-3483   _check_ai_models_sync
  9840-9883   _classify_pool_anonymity
  9886-9903   _classify_pool_anonymity_bg
   853-875    _claude_chat_sync_metered
  9086-9093   _client_ip
 20141-20168  _clip_prune
 20171-20181  _clip_recfile_for
 20591-20597  _clip_should_velocity
 20222-20304  _clip_to_discord
  3364-3373   _close_ai_session
 21121-21136  _cohost_broadcast
 21106-21107  _cohost_cfg
 21162-21174  _cohost_fire_highlight
 21110-21118  _cohost_gate
 21139-21159  _cohost_highlight
  9488-9490   _conv_messages
  6406-6467   _cookie_alarm_loop
  2003-2008   _cookie_autofetch_info
  1986-1990   _cookie_autorefresh_info
  1889-1893   _cookie_header
  2020-2053   _cookies_selbst_holen
  3699-3711   _create_index_safe
 19084-19190  _crowdsec_status
 19030-19081  _crowdsec_via_lapi
 18934-18952  _cscli_bin
 18961-18974  _cscli_path
  6296-6321   _daily_summary_loop
 18992-19009  _darf_journal_lesen
 19567-19590  _db_maintenance_loop
  6265-6293   _db_vacuum_loop
 14783-14807  _detect_foreign_ad
  1534-1545   _diag_path_owner
 16044-16088  _director_finalize
 16985-16992  _director_for
 15993-16041  _director_mark
 20456-20459  _disc_state_get
 20462-20469  _disc_state_set
 19513-19522  _discord_bot_starten
 19477-19488  _discord_einladung_merken
 19525-19529  _discord_invite
 19491-19510  _discord_kontext
 20417-20453  _discord_live_thread
 16195-16207  _discord_notify
 19449-19474  _discord_ops_alert
 20315-20413  _discord_post_user
 20060-20066  _discord_stop
  6324-6401   _disk_alarm_loop
 22567-22616  _disk_autoclean
 22619-22632  _disk_guard_loop
 12701-12708  _drossel_hoeher
 12697-12698  _drossel_stufe
 12711-12719  _drossel_zuruecksetzen
 11078-11080  _dump_all_threads
  9766-9829   _enrich_proxies_with_geo
  2082-2143   _ensure_cookie_file_netscape
  8183-8186   _ensure_notify_topic
 10010-10047  _ensure_proxy_ready
  8137-8164   _ensure_topic
   702-704    _env_int
   707-709    _env_int_range
 16240-16253  _event_webhook
 11751-11764  _evolution_loop
  5449-5483   _extract_file_payload
  2215-2217   _extract_urls_from_streamurl_node
 18977-18984  _f2b_sudo_hint
  4293-4303   _fehler_text
  9667-9685   _fetch_proxy_list
 16772-16800  _fetch_tiktok_room_id
   785-788    _ff_cmd
 12530-12535  _find_chromium
  3088-3090   _find_external_recorder
  2220-2222   _find_stream_urls
 11451-11476  _fire_webhooks
  7233-7242   _fork_safe
   886-899    _freeai_chat_sync_metered
 19023-19027  _geo_lookup_ips
  3352-3361   _get_ai_session
  7066-7106   _get_live_info
  2802-2809   _get_resolve_semaphore
  7466-7838   _handle_single_tracking
 22389-22391  _hb
 22394-22411  _hb_while
 12007-12009  _highlight_cfg
 12012-12041  _highlight_observe
 12538-12556  _htmlov_screenshot_cmd
 16499-16509  _httpx_proxy
 11484-11496  _in_quiet_hours
 23526-23557  _install_fast_eventloop
  8952-9006   _install_fast_json
 11083-11099  _install_faulthandler
 17713-17722  _intel_ensure_schema
 17760-17795  _intel_index_loop
 17734-17744  _intel_index_one
 17725-17731  _intel_semantic
  4818-4827   _is_authorized
  7367-7373   _is_dead
  2205-2207   _is_hevc
 19012-19014  _is_private_ip
  1698-1705   _is_process_running
  6037-6044   _is_quiet_hours
  1327-1336   _is_upload_window
  4158-4173   _iso
  9041-9054   _json_error_handler
  6259-6260   _kick_broadcaster_id
  6171-6213   _kick_follower_count
  6155-6158   _kick_slug
 10600-10607  _kick_user_token
 22988-22997  _kickmod_boot
  3748-3751   _kind_from_filename
 11513-11515  _latest_popularity
 17381-17430  _live_react_loop
 17058-17370  _live_react_worker
 15643-15654  _live_transcript_push
 17372-17379  _live_users
 16091-16135  _living_title_loop
 19733-19805  _local_backup_scan
  9023-9037   _log_5xx
   775-782    _log_sicher
 13095-13107  _looks_like_codec_err
 13090-13092  _looks_like_source_expired
  7283-7313   _loop_fehler
 11103-11112  _loop_heartbeat
 22359-22386  _loop_lag_monitor
 11115-11183  _loop_watchdog_thread
 15523-15537  _loyalty_add
 15514-15520  _loyalty_get
 15540-15548  _loyalty_top
 11623-11625  _manual_donations_total
  4500-4519   _manual_status
  7375-7376   _mark_dead
 10286-10302  _marketing_loop
 21022-21040  _maybe_handle_command
 22718-22742  _maybe_hype_clip
 20110-20138  _meme_klassifizieren
  3666-3689   _migrate_columns
 21301-21312  _mod_is_exempt
 21315-21320  _mod_warn_first
 21323-21326  _mod_warn_text
 11791-11799  _modlog
  1027-1029   _multistream_targets
  7245-7246   _nc_create_subprocess_exec
  7249-7250   _nc_create_subprocess_shell
 10537-10554  _news_loop
 11818-11820  _normalize_ingest
  2435-2452   _note_check_duration
  8177-8180   _notify_topic_name
 15669-15677  _oracle_memories
 15942-15976  _oracle_memorize
 15680-15693  _oracle_persona
 15662-15666  _oracle_recent_text
 12164-12165  _ov_atomic_write
 12155-12157  _ov_bar
 14686-14698  _ov_clip_text
 12160-12161  _ov_oneline
 18689-18718  _overlay_push
 12484-12527  _overlay_render_size
 11887-11891  _overlay_session_reset
 18654-18656  _overlay_src_ok
 14770-14780  _own_invites
 12479-12481  _parse_size
 19198-19278  _parse_ssh_attacks
  6668-6701   _pause_resume_cmd
  1940-1984   _persist_refreshed_cookies
  1843-1875   _pick_checked_pull_proxy
  9122-9135   _pin_auth_value
  9181-9182   _pin_clear_fail
  9161-9164   _pin_locked
  9167-9178   _pin_note_fail
  9138-9158   _pin_ok
 18498-18523  _piper_pick_model
 18583-18632  _piper_say
 11413-11448  _post_json_threaded
 12458-12476  _probe_video_size
  1726-1743   _proc_is_recorder
  9979-10007  _proxy_pool_refresh_loop
  1809-1840   _proxy_report_recording
 11068-11070  _prune_stall_dumps
 10356-10477  _public_stats
  2011-2017   _pull_proxy_still
 16211-16237  _push_notify
  9283-9285   _pwa_dir
  9736-9751   _quick_validate_proxy
 11479-11481  _quiet_hours_config
  9248-9281   _rate_guard
 15484-15490  _react_warn
  7153-7192   _reap_proc
  8407-8474   _rec_auto_abschalten
  8354-8404   _rec_frueh_getrennt
  8241-8299   _rec_kategorie_melden
  8302-8351   _rec_totstreak_fortschreiben
  2475-2497   _record_check_outcome
   770-772    _redact_stream_urls
  9906-9976   _refresh_proxy_pool
  2252-2343   _resolve_via_html
  2611-2779   _resolve_via_webcast_api_v2
  2842-2909   _resolve_via_ytdlp
 20631-20760  _resolve_youtube_ingest
  2231-2249   _resolver_stumm
 11870-11881  _restream_active_sources
 12807-12931  _restream_avatar_feeder_start
 12934-12943  _restream_avatar_feeder_stop
 16831-16949  _restream_chat_guardian
 12044-12116  _restream_chat_push
 12141-12150  _restream_chat_push_async
 12559-12668  _restream_html_overlay_start
 12671-12684  _restream_html_overlay_stop
 11829-11852  _restream_overlay_files
 17434-17466  _restream_platform_state
 17629-17664  _restream_resume_after_restart
 12991-13049  _restream_tts_enqueue_wav
 12420-12452  _restream_tts_feeder
 12417-12418  _restream_tts_fifo_path
 12946-12973  _restream_tts_start
 12975-12989  _restream_tts_stop
 17472-17626  _restream_verify_loop
 19698-19710  _retention_loop
 19692-19695  _retention_scan
  2573-2575   _room_is_abo
  5487-5604   _run_ai_call
 11206-11219  _run_async_from_flask
 19017-19020  _run_priv
 23514-23522  _run_selfcheck_and_exit
 19713-19724  _s3_client
  7402-7453   _safe_send
  4426-4442   _sample_net_throughput
  2527-2548   _schedule_next_check
 19646-19689  _scheduler_loop
  3692-3696   _schema_pk
 11223-11228  _scraper_session
 21329-21368  _screen_full
 10651-10688  _sec_headers
  2210-2212   _select_stream_from_data_section
 23302-23511  _selfcheck
  8189-8223   _send_live_notice
  1350-1354   _should_defer_upload
 20184-20219  _shrink_for_discord
  9288-9300   _sicheres_ziel
 19544-19564  _sicherheits_erinnerung_loop
 22639-22656  _sign_health_check
 22659-22678  _sign_health_loop
  4176-4201   _sitzung_bestimmen
  7262-7273   _spawn
 23932-23962  _spawn_from_flask
 16511-16769  _start_chat_listener
 11186-11203  _start_loop_watchdog
 10504-10532  _stats_loop
 10483-10486  _stats_output_path
 10489-10501  _stats_write
 18535-18549  _stimme_saubern
 18556-18580  _stimme_schon_gesagt
  7917-7933   _storage_cleanup_loop
 22698-22705  _story_for
  3113-3119   _stream_url_expiry
  3121-3126   _stream_url_ttl
 14733-14740  _streamer_persona_get
 19830-19952  _system_backup
 19961-19991  _system_backup_loop
 11028-11046  _task_auf_bot_schleife
  9688-9727   _test_proxy
 10234-10250  _testpush_resolve_live
  7378-7399   _tg_sprache_setzen
  8096-8106   _tg_topics_load_into_mem
  8093-8094   _tg_topics_path
  8108-8115   _tg_topics_save
  9096-9104   _token_ok
  8118-8122   _topic_forget
 11499-11510  _tracking_max_duration
  3956-3970   _tracking_remove_cleanup
  3987-3999   _tracking_resume_cleanup
  1592-1615   _try_attach_file_handler
 18525-18533  _tts_cleanup
 10210-10214  _tunnel_effective
 18021-18074  _twitch_channel_status
 21371-21516  _twitch_chat_loop
 20475-20488  _twitch_clip_versuchen
 21185-21288  _twitch_eventsub_loop
  1373-1386   _upload_queue_add
  1397-1399   _upload_queue_count
  1356-1365   _upload_queue_load
  1346-1348   _upload_queue_path
  1388-1395   _upload_queue_remove
  1367-1371   _upload_queue_save
  1401-1442   _upload_window_loop
  7126-7133   _uptime_s
 11806-11815  _url_host
   846-850    _usage_record_claude
 22812-22834  _v37_pause_source
 22776-22786  _v37_restream_restart
 22789-22809  _v37_unpause_source
  7316-7360   _verbindung_verloren
  6216-6247   _viewer_sample_loop
  9185-9188   _wants_html
  7136-7150   _warn_empty_env
 22432-22553  _watchdog_loop
 20906-20914  _wchat_thank_ok
 16279-16309  _whisper_get_model
  7223-7230   _whisper_native_section
 15471-15477  _whisper_pool
 16403-16435  _whisper_segments
 16311-16327  _whisper_stumm
 16330-16400  _whisper_transcribe
 12212-12374  _write_restream_overlay
 12174-12209  _write_restream_overlay_async
 21540-21636  _youtube_api_chat_loop
 18077-18180  _youtube_api_status
 18183-18250  _youtube_channel_status
 21639-21800  _youtube_chat_loop
 20491-20516  _youtube_clip_versuchen
 20766-20779  _youtube_restream_autoconfig
 20782-20806  _youtube_restream_autoconfig_inner
 20873-20901  _youtube_send
 18318-18359  _youtube_set_channel
 20809-20843  _yt_access_token
 20846-20861  _yt_live_chat_id
 20869-20870  _yt_sendrate_cfg
 21519-21534  _yt_timeout
  2826-2827   _ytdlp_detect_available
  2829-2840   _ytdlp_note_result
 11073-11075  _zombie_child_count
  7002-7026   about
  3867-3871   add_ai_log_entry
  3784-3787   add_archive_entry
  4464-4466   add_archive_rule
  4204-4275   add_recording
  3931-3948   add_tracking
  5607-5640   ai
  3497-3570   ai_chat
  3604-3614   ai_history_append
  3616-3621   ai_history_clear
  3593-3602   ai_history_load
  3578-3591   ai_rate_limit_check
  5669-5677   aireset
 15810-15829  azrael_chat
 21805-21927  brain_cmd
  3129-3134   build_recording_cmd
  3951-3954   bulk_add_trackings
  6470-6529   bulkadd
  7936-8076   check_all_trackings
  4003-4015   claim_live_transition
 14810-15403  class KickModerator
 13110-14573  class RestreamManager
 10093-10135  classify_proxy_anonymity
  5715-5913   cleanup
  4754-4760   cleanup_old_recordings
  4149-4156   clear_recording
 20519-20588  clip_moment
  4416-4419   compute_storage_forecast
  6592-6665   cookies_cmd
  3922-3928   count_trackings_for_chat
  3854-3865   decide_preferred_recorder
  3794-3797   delete_archive_entry
  4468-4470   delete_archive_rule
  5144-5291   diag
 22039-22100  einnahmen_cmd
  4410-4413   find_recordings_by_fingerprint
  3815-3831   finish_recording_attempt
  3975-3977   get_all_active_trackings
  3882-3884   get_all_checks
  4277-4280   get_all_recordings
  4359-4361   get_all_tags_with_counts
  4387-4390   get_annotations_for_recording
  3789-3792   get_archive_entry
  4380-4383   get_bookmarked_recordings
  2070-2075   get_cookie_health
  4347-4353   get_event_log
  3838-3852   get_last_recording_attempt
  2912-3050   get_live_status
  4693-4696   get_manual_recordings
  4395-4398   get_or_compute_inspect_sync
  4795-4798   get_outcome_breakdown
  4366-4369   get_priority_poll_interval
  3833-3836   get_recent_recording_attempts
  4282-4285   get_recording_by_id
  4373-4376   get_recording_note
  3298-3321   get_redis
  3911-3914   get_stats
  4748-4752   get_storage_stats
  4488-4490   get_tiktok_status_distribution
  4017-4026   get_tracking_state
  3972-3973   get_trackings_for_group
  4709-4712   get_trash_recordings
  8477-8931   handle_recording_finished
  3714-3739   init_db
  4460-4462   list_archive_rules
  4948-4986   live
  7456-7464   live_check_worker
  3376-3410   llm_chat
  3433-3461   llm_chat_sync
  3418-3430   llm_list_models
  4306-4339   log_event
  1660-1693   log_recording_failure
  6815-6864   logs_cmd
 23000-23292  main
  5643-5666   on_ai_media
  6941-6967   on_ai_reply
  6970-6999   on_azrael_mention
  7031-7061   on_callback
 15835-15939  oracle_handle
  6704-6707   pause_tracking
  4808-4813   profile_keyboard
  6766-6812   quota
  7840-7914   reaper_loop
  4484-4486   record_tiktok_status
  5682-5712   recstatus
  3323-3331   redis_get_json
  3334-3340   redis_set_json
 22103-22113  report_cmd
 10138-10140  report_proxy_result
  2346-2388   resolve_tiktok_live_stream
  4704-4707   restore_recording
  6710-6713   resume_tracking
  4473-4478   run_archive_rules
 22116-22339  run_bot
 10967-11019  run_flask
  4448-4451   sample_bandwidth_for_active
  3874-3880   save_tiktok_check
  4141-4147   set_recording_file
  3980-3984   set_tracking_paused
  4699-4702   soft_delete_recording
  8229-8239   split_and_send_video
  4861-4903   start
  3799-3813   start_recording_attempt
  5916-5954   stats
  4638-4691   stop_manual_recording
  6716-6763   stoprec
  6140-6148   summary_cmd
  6867-6938   sysres
  5293-5437   teststream
  4905-4946   tiktok
  6532-6589   topusers
  5023-5080   track
  4988-5020   track_exact
  5094-5142   tracklist
  4522-4636   trigger_manual_recording
  4102-4139   try_acquire_recording_lock
  4715-4717   universal_search
  5082-5092   untrack
 21930-22036  update_cmd
  4405-4408   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, concat_cmd, concat_liste, gehoert_dazu, luecken, sekunden, sitzung_id, zieldatei
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, configure, oauth_exchange, search_category, send_message, slug, timeout_user, update_channel, user_token
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livefolge.py           braucht_url_nachschlag, hat_stream_url, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, schriftart
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
