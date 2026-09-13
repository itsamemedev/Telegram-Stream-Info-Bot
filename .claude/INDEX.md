# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9455  GET              /                                                dashboard
 11405  GET              /api/abo/status                                  api_abo_status
 11359  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10243  GET              /api/automation/status                           api_automation_status
 10265  POST             /api/automation/toggle                           api_automation_toggle
 18514  GET              /api/channel/categories                          api_channel_categories
 18520  POST             /api/channel/set                                 api_channel_set
 18367  GET              /api/channels/status                             api_channels_status
 18041  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18024  GET              /api/clips                                       api_clips
 18070  POST/DELETE      /api/clips/clear                                 api_clips_clear
 17949  GET              /api/debug/threads                               api_debug_threads
 11370  GET              /api/events                                      api_events
 10884  GET              /api/events/stream                               api_events_stream
 10711  GET              /api/health                                      api_health
 17983  POST             /api/highlights/config                           api_highlights_config
  9389  POST             /api/login                                       dashboard_login_submit
 11695  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 10799  GET              /api/notify/status                               api_notify_status
 10810  POST             /api/notify/test                                 api_notify_test
 11459  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11436  GET              /api/proxy/trend                                 api_proxy_trend
 18090  GET              /api/tts/<fn>                                    api_tts_file
 18865  GET              /api/upload_window                               api_upload_window
 11001  GET              /archive/<int:eid>/download                      archive_download
 11029  GET              /download/<int:recording_id>                     download
 10958  GET              /health                                          health
 17918  GET              /healthz                                         healthz
  9380  GET              /login                                           dashboard_login_page
  9410  GET              /logout                                          dashboard_logout
  9417  GET              /manifest.webmanifest                            pwa_manifest
 18838  GET              /overlay                                         overlay_page
  9441  GET              /pwa-icon-<variant>.png                          pwa_icon
  9427  GET              /sw.js                                           pwa_service_worker
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
  2573-2574   _abo_key
  2594-2612   _abo_probe_dump
 14873-14880  _ad_allowlist
 15849-15855  _agent_for
 15858-15874  _ai_telemetry
 16369-16387  _alert
 19724-19774  _alert_monitor_loop
 20126-20188  _announce_loop
  3205-3215   _anthropic_key
  3222-3224   _anthropic_model
  9094-9097   _arg_int
  2565-2570   _as_dict
 22895-22904  _async_exc_handler
 16550-16572  _audio_tap_cmd
 17109-17168  _audio_tap_melden
 16586-16610  _audio_tap_sammler
  9262-9312   _auth_cookie
  9229-9258   _auth_guard
  1802-1807   _auto_on
 17780-17798  _auto_restream_loop
 12875-12917  _avatar_frames_laden
 21206-21221  _azrael_broadcast_reply
 21106-21128  _azrael_chat_reply
 21078-21103  _azrael_chat_should_reply
 21134-21136  _azrael_gate_cfg
 15879-15893  _azrael_live_state
 18751-18765  _azrael_overlay_state
 16251-16305  _azrael_proactive_loop
 15697-15753  _azrael_reaction_to_chats
 21139-21146  _azrael_reply_all_chats
 21065-21075  _azrael_self_names
 21174-21203  _azrael_send_to
 12836-12872  _azrael_spricht
 15899-15920  _azrael_system
 19858-19861  _backup_active
 19939-19952  _backup_loop
 22968-22977  _brain_crowdsec_snap
 19645-19654  _brain_growth_loop
  9634-9661   _brain_growth_snapshot
  2507-2527   _brain_hint_delay
 23040-23075  _brain_moderation_snap
  6044-6072   _brain_notify
 23078-23100  _brain_recording_snap
 22980-23037  _brain_restream_health
 23103-23116  _brain_tiktok_status_snap
 10863-10880  _browser_push
  6084-6171   _build_daily_summary
 13196-13200  _build_restream_cmd
  4866-4893   _can_stop_tracking
  1915-1937   _capture_set_cookies
 11513-11516  _cfg_get
 11519-11521  _cfg_set
 18475-18510  _channel_set_all
 12064-12067  _chat_connected
 12070-12086  _chat_disconnected
  8161-8172   _chat_is_forum
 16916-16941  _chat_listener_abbauen
 12106-12108  _chat_sanitize
 12049-12061  _chat_stat
 12089-12092  _chat_stats_snapshot
  3508-3520   _check_ai_models_sync
  9916-9959   _classify_pool_anonymity
  9962-9979   _classify_pool_anonymity_bg
   855-877    _claude_chat_sync_metered
  9123-9130   _client_ip
 20272-20299  _clip_prune
 20302-20312  _clip_recfile_for
 20722-20728  _clip_should_velocity
 20353-20435  _clip_to_discord
  3401-3410   _close_ai_session
 21252-21267  _cohost_broadcast
 21237-21238  _cohost_cfg
 21293-21305  _cohost_fire_highlight
 21241-21249  _cohost_gate
 21270-21290  _cohost_highlight
  9564-9566   _conv_messages
  6443-6504   _cookie_alarm_loop
  2006-2011   _cookie_autofetch_info
  1989-1993   _cookie_autorefresh_info
  1892-1896   _cookie_header
  2023-2056   _cookies_selbst_holen
  3736-3748   _create_index_safe
 19197-19303  _crowdsec_status
 19143-19194  _crowdsec_via_lapi
 19047-19065  _cscli_bin
 19074-19087  _cscli_path
  6333-6358   _daily_summary_loop
 19105-19122  _darf_journal_lesen
 19698-19721  _db_maintenance_loop
  6302-6330   _db_vacuum_loop
 14896-14920  _detect_foreign_ad
  1537-1548   _diag_path_owner
 16157-16201  _director_finalize
 17098-17105  _director_for
 16106-16154  _director_mark
 20587-20590  _disc_state_get
 20593-20600  _disc_state_set
 19626-19635  _discord_bot_starten
 19590-19601  _discord_einladung_merken
 19638-19642  _discord_invite
 19604-19623  _discord_kontext
 20548-20584  _discord_live_thread
 16308-16320  _discord_notify
 19562-19587  _discord_ops_alert
 20446-20544  _discord_post_user
 20191-20197  _discord_stop
  6361-6438   _disk_alarm_loop
 22698-22747  _disk_autoclean
 22750-22763  _disk_guard_loop
 12814-12821  _drossel_hoeher
 12810-12811  _drossel_stufe
 12824-12832  _drossel_zuruecksetzen
 11191-11193  _dump_all_threads
  9842-9905   _enrich_proxies_with_geo
  2085-2146   _ensure_cookie_file_netscape
  8220-8223   _ensure_notify_topic
 10086-10123  _ensure_proxy_ready
  8174-8201   _ensure_topic
   704-706    _env_int
   709-711    _env_int_range
 16353-16366  _event_webhook
 11864-11877  _evolution_loop
  5486-5520   _extract_file_payload
  2218-2220   _extract_urls_from_streamurl_node
 19090-19097  _f2b_sudo_hint
  4330-4340   _fehler_text
  9743-9761   _fetch_proxy_list
 16885-16913  _fetch_tiktok_room_id
   787-790    _ff_cmd
 12643-12648  _find_chromium
  3125-3127   _find_external_recorder
  2223-2225   _find_stream_urls
 11564-11589  _fire_webhooks
  7270-7279   _fork_safe
   888-901    _freeai_chat_sync_metered
 19136-19140  _geo_lookup_ips
  3389-3398   _get_ai_session
  7103-7143   _get_live_info
  2839-2846   _get_resolve_semaphore
  7503-7875   _handle_single_tracking
 22520-22522  _hb
 22525-22542  _hb_while
 12120-12122  _highlight_cfg
 12125-12154  _highlight_observe
 12651-12669  _htmlov_screenshot_cmd
 16612-16622  _httpx_proxy
 11597-11609  _in_quiet_hours
 23664-23695  _install_fast_eventloop
  8989-9043   _install_fast_json
 11196-11212  _install_faulthandler
 17826-17835  _intel_ensure_schema
 17873-17908  _intel_index_loop
 17847-17857  _intel_index_one
 17838-17844  _intel_semantic
  4855-4864   _is_authorized
  7404-7410   _is_dead
  2208-2210   _is_hevc
 19125-19127  _is_private_ip
  1701-1708   _is_process_running
  6074-6081   _is_quiet_hours
  1330-1339   _is_upload_window
  4195-4210   _iso
  9078-9091   _json_error_handler
  6296-6297   _kick_broadcaster_id
  6208-6250   _kick_follower_count
  6192-6195   _kick_slug
 10676-10683  _kick_user_token
 23119-23128  _kickmod_boot
  3785-3788   _kind_from_filename
 11626-11628  _latest_popularity
 17494-17543  _live_react_loop
 17171-17483  _live_react_worker
 15756-15767  _live_transcript_push
 17485-17492  _live_users
 16204-16248  _living_title_loop
 19864-19936  _local_backup_scan
  9060-9074   _log_5xx
   777-784    _log_sicher
 13208-13220  _looks_like_codec_err
 13203-13205  _looks_like_source_expired
  7320-7350   _loop_fehler
 11216-11225  _loop_heartbeat
 22490-22517  _loop_lag_monitor
 11228-11296  _loop_watchdog_thread
 15636-15650  _loyalty_add
 15627-15633  _loyalty_get
 15653-15661  _loyalty_top
 11736-11738  _manual_donations_total
  4537-4556   _manual_status
  7412-7413   _mark_dead
 10362-10378  _marketing_loop
 21153-21171  _maybe_handle_command
 22849-22873  _maybe_hype_clip
 20241-20269  _meme_klassifizieren
  3703-3726   _migrate_columns
 21432-21443  _mod_is_exempt
 21446-21451  _mod_warn_first
 21454-21457  _mod_warn_text
 11904-11912  _modlog
  1030-1032   _multistream_targets
  7282-7283   _nc_create_subprocess_exec
  7286-7287   _nc_create_subprocess_shell
 10613-10630  _news_loop
 11931-11933  _normalize_ingest
  2438-2455   _note_check_duration
  8214-8217   _notify_topic_name
 15782-15790  _oracle_memories
 16055-16089  _oracle_memorize
 15793-15806  _oracle_persona
 15775-15779  _oracle_recent_text
 12277-12278  _ov_atomic_write
 12268-12270  _ov_bar
 14799-14811  _ov_clip_text
 12273-12274  _ov_oneline
 18802-18831  _overlay_push
 12597-12640  _overlay_render_size
 12000-12004  _overlay_session_reset
 18767-18769  _overlay_src_ok
 14883-14893  _own_invites
 12592-12594  _parse_size
 19311-19391  _parse_ssh_attacks
  6705-6738   _pause_resume_cmd
  1943-1987   _persist_refreshed_cookies
  1846-1878   _pick_checked_pull_proxy
  9159-9172   _pin_auth_value
  9218-9219   _pin_clear_fail
  9198-9201   _pin_locked
  9204-9215   _pin_note_fail
  9175-9195   _pin_ok
 18611-18636  _piper_pick_model
 18696-18745  _piper_say
 11526-11561  _post_json_threaded
 12571-12589  _probe_video_size
  1729-1746   _proc_is_recorder
 10055-10083  _proxy_pool_refresh_loop
  1812-1843   _proxy_report_recording
 11181-11183  _prune_stall_dumps
 10432-10553  _public_stats
  2014-2020   _pull_proxy_still
 16324-16350  _push_notify
  9359-9361   _pwa_dir
  9812-9827   _quick_validate_proxy
 11592-11594  _quiet_hours_config
  9324-9357   _rate_guard
 15597-15603  _react_warn
  7190-7229   _reap_proc
  8444-8511   _rec_auto_abschalten
  8391-8441   _rec_frueh_getrennt
  8278-8336   _rec_kategorie_melden
  8339-8388   _rec_totstreak_fortschreiben
  2478-2500   _record_check_outcome
   772-774    _redact_stream_urls
  9982-10052  _refresh_proxy_pool
  2255-2346   _resolve_via_html
  2619-2816   _resolve_via_webcast_api_v2
  2879-2946   _resolve_via_ytdlp
 20762-20891  _resolve_youtube_ingest
  2234-2252   _resolver_stumm
 11983-11994  _restream_active_sources
 12920-13044  _restream_avatar_feeder_start
 13047-13056  _restream_avatar_feeder_stop
 16944-17062  _restream_chat_guardian
 12157-12229  _restream_chat_push
 12254-12263  _restream_chat_push_async
 12672-12781  _restream_html_overlay_start
 12784-12797  _restream_html_overlay_stop
 11942-11965  _restream_overlay_files
 17547-17579  _restream_platform_state
 17742-17777  _restream_resume_after_restart
 13104-13162  _restream_tts_enqueue_wav
 12533-12565  _restream_tts_feeder
 12530-12531  _restream_tts_fifo_path
 13059-13086  _restream_tts_start
 13088-13102  _restream_tts_stop
 17585-17739  _restream_verify_loop
 19829-19841  _retention_loop
 19823-19826  _retention_scan
  2576-2578   _room_is_abo
  5524-5641   _run_ai_call
 11319-11332  _run_async_from_flask
 19130-19133  _run_priv
 23652-23660  _run_selfcheck_and_exit
 19844-19855  _s3_client
  7439-7490   _safe_send
  4463-4479   _sample_net_throughput
  2530-2551   _schedule_next_check
 19777-19820  _scheduler_loop
  3729-3733   _schema_pk
 11336-11341  _scraper_session
 21460-21499  _screen_full
 10727-10764  _sec_headers
  2213-2215   _select_stream_from_data_section
 23440-23649  _selfcheck
  8226-8260   _send_live_notice
  1353-1357   _should_defer_upload
 20315-20350  _shrink_for_discord
  9364-9376   _sicheres_ziel
 19657-19695  _sicherheits_erinnerung_loop
 22770-22787  _sign_health_check
 22790-22809  _sign_health_loop
  4213-4238   _sitzung_bestimmen
  7299-7310   _spawn
 24070-24100  _spawn_from_flask
 16624-16882  _start_chat_listener
 11299-11316  _start_loop_watchdog
 10580-10608  _stats_loop
 10559-10562  _stats_output_path
 10565-10577  _stats_write
 18648-18662  _stimme_saubern
 18669-18693  _stimme_schon_gesagt
  7954-7970   _storage_cleanup_loop
 22829-22836  _story_for
  3150-3156   _stream_url_expiry
  3158-3163   _stream_url_ttl
 14846-14853  _streamer_persona_get
 19961-20083  _system_backup
 20092-20122  _system_backup_loop
 11141-11159  _task_auf_bot_schleife
  9764-9803   _test_proxy
 10310-10326  _testpush_resolve_live
  7415-7436   _tg_sprache_setzen
  8133-8143   _tg_topics_load_into_mem
  8130-8131   _tg_topics_path
  8145-8152   _tg_topics_save
  9133-9141   _token_ok
  8155-8159   _topic_forget
 11612-11623  _tracking_max_duration
  3993-4007   _tracking_remove_cleanup
  4024-4036   _tracking_resume_cleanup
  1595-1618   _try_attach_file_handler
 18638-18646  _tts_cleanup
 10286-10290  _tunnel_effective
 18134-18187  _twitch_channel_status
 21502-21647  _twitch_chat_loop
 20606-20619  _twitch_clip_versuchen
 21316-21419  _twitch_eventsub_loop
  1376-1389   _upload_queue_add
  1400-1402   _upload_queue_count
  1359-1368   _upload_queue_load
  1349-1351   _upload_queue_path
  1391-1398   _upload_queue_remove
  1370-1374   _upload_queue_save
  1404-1445   _upload_window_loop
  7163-7170   _uptime_s
 11919-11928  _url_host
   848-852    _usage_record_claude
 22943-22965  _v37_pause_source
 22907-22917  _v37_restream_restart
 22920-22940  _v37_unpause_source
  7353-7397   _verbindung_verloren
  6253-6284   _viewer_sample_loop
  9222-9225   _wants_html
  7173-7187   _warn_empty_env
 22563-22684  _watchdog_loop
 21037-21045  _wchat_thank_ok
 16392-16422  _whisper_get_model
  7260-7267   _whisper_native_section
 15584-15590  _whisper_pool
 16516-16548  _whisper_segments
 16424-16440  _whisper_stumm
 16443-16513  _whisper_transcribe
 12325-12487  _write_restream_overlay
 12287-12322  _write_restream_overlay_async
 21671-21767  _youtube_api_chat_loop
 18190-18293  _youtube_api_status
 18296-18363  _youtube_channel_status
 21770-21931  _youtube_chat_loop
 20622-20647  _youtube_clip_versuchen
 20897-20910  _youtube_restream_autoconfig
 20913-20937  _youtube_restream_autoconfig_inner
 21004-21032  _youtube_send
 18431-18472  _youtube_set_channel
 20940-20974  _yt_access_token
 20977-20992  _yt_live_chat_id
 21000-21001  _yt_sendrate_cfg
 21650-21665  _yt_timeout
  2863-2864   _ytdlp_detect_available
  2866-2877   _ytdlp_note_result
 11186-11188  _zombie_child_count
  7039-7063   about
  3904-3908   add_ai_log_entry
  3821-3824   add_archive_entry
  4501-4503   add_archive_rule
  4241-4312   add_recording
  3968-3985   add_tracking
  5644-5677   ai
  3534-3607   ai_chat
  3641-3651   ai_history_append
  3653-3658   ai_history_clear
  3630-3639   ai_history_load
  3615-3628   ai_rate_limit_check
  5706-5714   aireset
 15923-15942  azrael_chat
 21936-22058  brain_cmd
  3166-3171   build_recording_cmd
  3988-3991   bulk_add_trackings
  6507-6566   bulkadd
  7973-8113   check_all_trackings
  4040-4052   claim_live_transition
 14923-15516  class KickModerator
 13223-14686  class RestreamManager
 10169-10211  classify_proxy_anonymity
  5752-5950   cleanup
  4791-4797   cleanup_old_recordings
  4186-4193   clear_recording
 20650-20719  clip_moment
  4453-4456   compute_storage_forecast
  6629-6702   cookies_cmd
  3959-3965   count_trackings_for_chat
  3891-3902   decide_preferred_recorder
  3831-3834   delete_archive_entry
  4505-4507   delete_archive_rule
  5181-5328   diag
 22170-22231  einnahmen_cmd
  4447-4450   find_recordings_by_fingerprint
  3852-3868   finish_recording_attempt
  4012-4014   get_all_active_trackings
  3919-3921   get_all_checks
  4314-4317   get_all_recordings
  4396-4398   get_all_tags_with_counts
  4424-4427   get_annotations_for_recording
  3826-3829   get_archive_entry
  4417-4420   get_bookmarked_recordings
  2073-2078   get_cookie_health
  4384-4390   get_event_log
  3875-3889   get_last_recording_attempt
  2949-3087   get_live_status
  4730-4733   get_manual_recordings
  4432-4435   get_or_compute_inspect_sync
  4832-4835   get_outcome_breakdown
  4403-4406   get_priority_poll_interval
  3870-3873   get_recent_recording_attempts
  4319-4322   get_recording_by_id
  4410-4413   get_recording_note
  3335-3358   get_redis
  3948-3951   get_stats
  4785-4789   get_storage_stats
  4525-4527   get_tiktok_status_distribution
  4054-4063   get_tracking_state
  4009-4010   get_trackings_for_group
  4746-4749   get_trash_recordings
  8514-8968   handle_recording_finished
  3751-3776   init_db
  4497-4499   list_archive_rules
  4985-5023   live
  7493-7501   live_check_worker
  3413-3447   llm_chat
  3470-3498   llm_chat_sync
  3455-3467   llm_list_models
  4343-4376   log_event
  1663-1696   log_recording_failure
  6852-6901   logs_cmd
 23131-23430  main
  5680-5703   on_ai_media
  6978-7004   on_ai_reply
  7007-7036   on_azrael_mention
  7068-7098   on_callback
 15948-16052  oracle_handle
  6741-6744   pause_tracking
  4845-4850   profile_keyboard
  6803-6849   quota
  7877-7951   reaper_loop
  4521-4523   record_tiktok_status
  5719-5749   recstatus
  3360-3368   redis_get_json
  3371-3377   redis_set_json
 22234-22244  report_cmd
 10214-10216  report_proxy_result
  2349-2391   resolve_tiktok_live_stream
  4741-4744   restore_recording
  6747-6750   resume_tracking
  4510-4515   run_archive_rules
 22247-22470  run_bot
 11043-11132  run_flask
  4485-4488   sample_bandwidth_for_active
  3911-3917   save_tiktok_check
  4178-4184   set_recording_file
  4017-4021   set_tracking_paused
  4736-4739   soft_delete_recording
  8266-8276   split_and_send_video
  4898-4940   start
  3836-3850   start_recording_attempt
  5953-5991   stats
  4675-4728   stop_manual_recording
  6753-6800   stoprec
  6177-6185   summary_cmd
  6904-6975   sysres
  5330-5474   teststream
  4942-4983   tiktok
  6569-6626   topusers
  5060-5117   track
  5025-5057   track_exact
  5131-5179   tracklist
  4559-4673   trigger_manual_recording
  4139-4176   try_acquire_recording_lock
  4752-4754   universal_search
  5119-5129   untrack
 22061-22167  update_cmd
  4442-4445   update_recording_fingerprint
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
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
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
webserver.py           bindung, ist_loopback, threads, waehle
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
