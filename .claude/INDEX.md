# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
  9959  GET              /                                                dashboard
 11875  GET              /api/abo/status                                  api_abo_status
 11829  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10747  GET              /api/automation/status                           api_automation_status
 10769  POST             /api/automation/toggle                           api_automation_toggle
 18613  GET              /api/channel/categories                          api_channel_categories
 18619  POST             /api/channel/set                                 api_channel_set
 18466  GET              /api/channels/status                             api_channels_status
 18140  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18123  GET              /api/clips                                       api_clips
 18169  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18048  GET              /api/debug/threads                               api_debug_threads
 11840  GET              /api/events                                      api_events
 11412  GET              /api/events/stream                               api_events_stream
 11239  GET              /api/health                                      api_health
 18082  POST             /api/highlights/config                           api_highlights_config
  9893  POST             /api/login                                       dashboard_login_submit
 12168  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11327  GET              /api/notify/status                               api_notify_status
 11338  POST             /api/notify/test                                 api_notify_test
 11929  GET              /api/proxy/heatmap                               api_proxy_heatmap
 11906  GET              /api/proxy/trend                                 api_proxy_trend
 18189  GET              /api/tts/<fn>                                    api_tts_file
 18915  GET              /api/upload_window                               api_upload_window
 11529  GET              /archive/<int:eid>/download                      archive_download
 11557  GET              /download/<int:recording_id>                     download
 11486  GET              /health                                          health
 18017  GET              /healthz                                         healthz
  9884  GET              /login                                           dashboard_login_page
  9914  GET              /logout                                          dashboard_logout
  9921  GET              /manifest.webmanifest                            pwa_manifest
 18888  GET              /overlay                                         overlay_page
  9945  GET              /pwa-icon-<variant>.png                          pwa_icon
  9931  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (327)

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
   832  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   914  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   942  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   953  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   819  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   881  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   868  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   849  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   319  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   494  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   489  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   537  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   420  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   747  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   511  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   474  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   447  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   721  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   591  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   680  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   586  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   519  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   299  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   764  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   387  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   642  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   797  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   782  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   343  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   581  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   567  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   550  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   607  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   700  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   596  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
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

## Discord-Slash-Commands (45)

```
 19908  /ai                     
 20381  /ask                    
 19999  /assign_role            
 20045  /ban                    
 20713  /botstats               
 20637  /clearwarns             
 20677  /clip                   
 20662  /clipoftheweek          
 20504  /clips                  
 19960  /create_category        
 19929  /create_channel         
 19988  /create_group           
 19971  /create_role            
 19945  /create_voice           
 20281  /daily                  
 20411  /event                  
 20454  /events                 
 20550  /follow                 
 20534  /help                   
 20034  /kick                   
 20263  /leaderboard            
 20490  /livenow                
 20520  /post_test              
 20351  /profile                
 20069  /purge                  
 20249  /rank                   
 20477  /recstatus              
 20010  /remove_role            
 19922  /restream_status        
 20021  /set_channel_perms      
 20214  /setup_community        
 20232  /setup_targets          
 20576  /stats                  
 19834  /status                 
 20872  /streaminfo             
 20769  /sys_report             
 20745  /sys_unpause            
 20056  /timeout                
 20648  /topstreamers           
 19864  /track                  
 19848  /tracklist              
 20565  /unfollow               
 19897  /untrack                
 20598  /warn                   
 20622  /warnings               
```

## Discord-Events (4)

```
 21370  on_member_join
 21332  on_message
 20959  on_raw_reaction_add
 21405  on_ready
```

## Top-Level-Symbole in bot.py (471 Funktionen, 2 Klassen)

```
  2610-2611   _abo_key
  2631-2649   _abo_probe_dump
 15178-15185  _ad_allowlist
 16319-16325  _agent_for
 16328-16344  _ai_telemetry
 16833-16851  _alert
 21544-21594  _alert_monitor_loop
 21946-22008  _announce_loop
  3552-3555   _anthropic_key
  3562-3564   _anthropic_model
  9637-9640   _arg_int
  2602-2607   _as_dict
 16986-17008  _audio_tap_cmd
  9805-9816   _auth_cookie
  9772-9801   _auth_guard
  1724-1729   _auto_on
 17879-17897  _auto_restream_loop
 23087-23102  _azrael_broadcast_reply
 22987-23009  _azrael_chat_reply
 22970-22984  _azrael_chat_should_reply
 23015-23017  _azrael_gate_cfg
 16349-16363  _azrael_live_state
 18800-18814  _azrael_overlay_state
 16715-16769  _azrael_proactive_loop
 16167-16223  _azrael_reaction_to_chats
 23020-23027  _azrael_reply_all_chats
 22957-22967  _azrael_self_names
 23055-23084  _azrael_send_to
 16369-16390  _azrael_system
 21678-21681  _backup_active
 21759-21772  _backup_loop
 21483-21492  _brain_growth_loop
 10138-10165  _brain_growth_snapshot
  2538-2558   _brain_hint_delay
  6230-6258   _brain_notify
 11391-11408  _browser_push
  6274-6361   _build_daily_summary
  3041-3221   _build_native_cmd
 13364-13551  _build_restream_cmd
  3265-3298   _build_ytdlp_cmd
  5052-5079   _can_stop_tracking
  1837-1859   _capture_set_cookies
 11983-11986  _cfg_get
 11989-11991  _cfg_set
 18574-18609  _channel_set_all
 12522-12525  _chat_connected
 12528-12544  _chat_disconnected
  8356-8367   _chat_is_forum
 12564-12566  _chat_sanitize
 12507-12519  _chat_stat
 12547-12550  _chat_stats_snapshot
  3835-3847   _check_ai_models_sync
 10420-10463  _classify_pool_anonymity
 10466-10483  _classify_pool_anonymity_bg
   823-845    _claude_chat_sync_metered
  9666-9673   _client_ip
 22040-22067  _clip_prune
 22070-22080  _clip_recfile_for
 22621-22627  _clip_should_velocity
 22121-22203  _clip_to_discord
  3728-3737   _close_ai_session
 23133-23148  _cohost_broadcast
 23118-23119  _cohost_cfg
 23174-23186  _cohost_fire_highlight
 23122-23130  _cohost_gate
 23151-23171  _cohost_highlight
 22252-22314  _community_events_loop
 10068-10070  _conv_messages
  6633-6694   _cookie_alarm_loop
  1928-1933   _cookie_autofetch_info
  1911-1915   _cookie_autorefresh_info
  1814-1818   _cookie_header
  1945-1978   _cookies_selbst_holen
  4041-4053   _create_index_safe
 19247-19353  _crowdsec_status
 19193-19244  _crowdsec_via_lapi
 19097-19115  _cscli_bin
 19124-19137  _cscli_path
  6523-6548   _daily_summary_loop
 19155-19172  _darf_journal_lesen
 21518-21541  _db_maintenance_loop
  6492-6520   _db_vacuum_loop
 15201-15225  _detect_foreign_ad
  1459-1470   _diag_path_owner
 16621-16665  _director_finalize
 17432-17439  _director_for
 16570-16618  _director_mark
 22515-22550  _disc_automod_check
 22491-22494  _disc_state_get
 22497-22504  _disc_state_set
 19691-19695  _discord_invite
 22452-22488  _discord_live_thread
 16772-16784  _discord_notify
 19590-19615  _discord_ops_alert
 22350-22448  _discord_post_user
 19751-21480  _discord_run_once
 19630-19688  _discord_start
 22011-22017  _discord_stop
  6551-6628   _disk_alarm_loop
 24563-24612  _disk_autoclean
 24615-24628  _disk_guard_loop
 12957-12959  _drawtext_chain
 11661-11663  _dump_all_threads
 10346-10409  _enrich_proxies_with_geo
  2153-2214   _ensure_cookie_file_netscape
 19698-19748  _ensure_discord_invite
 22217-22249  _ensure_error_channel
  8415-8418   _ensure_notify_topic
 10590-10627  _ensure_proxy_ready
  8369-8396   _ensure_topic
   688-690    _env_int
   693-695    _env_int_range
 22317-22347  _error_channel_loop
 16817-16830  _event_webhook
 12337-12350  _evolution_loop
  5672-5706   _extract_file_payload
  2286-2288   _extract_urls_from_streamurl_node
 19140-19147  _f2b_sudo_hint
  4552-4562   _fehler_text
 10247-10265  _fetch_proxy_list
 17266-17294  _fetch_tiktok_room_id
   756-759    _ff_cmd
 13123-13128  _find_chromium
  3258-3262   _find_external_recorder
  2291-2293   _find_stream_urls
 12034-12059  _fire_webhooks
  7460-7469   _fork_safe
   856-869    _freeai_chat_sync_metered
 19186-19190  _geo_lookup_ips
  3716-3725   _get_ai_session
  7293-7333   _get_live_info
  2828-2835   _get_resolve_semaphore
  7693-8070   _handle_single_tracking
 24385-24387  _hb
 24390-24407  _hb_while
 12578-12580  _highlight_cfg
 12583-12612  _highlight_observe
 13131-13149  _htmlov_screenshot_cmd
 17010-17020  _httpx_proxy
 12067-12079  _in_quiet_hours
 25454-25485  _install_fast_eventloop
  9532-9586   _install_fast_json
 11666-11682  _install_faulthandler
 17925-17934  _intel_ensure_schema
 17972-18007  _intel_index_loop
 17946-17956  _intel_index_one
 17937-17943  _intel_semantic
  5041-5050   _is_authorized
  7594-7600   _is_dead
  2276-2278   _is_hevc
 19175-19177  _is_private_ip
  1623-1630   _is_process_running
  6260-6271   _is_quiet_hours
  1252-1261   _is_upload_window
  9621-9634   _json_error_handler
  6486-6487   _kick_broadcaster_id
  6398-6440   _kick_follower_count
  6382-6385   _kick_slug
 11180-11211  _kick_user_token
  4090-4093   _kind_from_filename
 12096-12101  _latest_popularity
 17647-17680  _live_react_loop
 17443-17636  _live_react_worker
 16226-16237  _live_transcript_push
 17638-17645  _live_users
 16668-16712  _living_title_loop
 21684-21756  _local_backup_scan
  9603-9617   _log_5xx
 13559-13571  _looks_like_codec_err
 13554-13556  _looks_like_source_expired
  7510-7540   _loop_fehler
 11686-11695  _loop_heartbeat
 24355-24382  _loop_lag_monitor
 11698-11766  _loop_watchdog_thread
 16106-16120  _loyalty_add
 16097-16103  _loyalty_get
 16123-16131  _loyalty_top
 12209-12211  _manual_donations_total
  4759-4778   _manual_status
  7602-7603   _mark_dead
 10866-10882  _marketing_loop
 23034-23052  _maybe_handle_command
 24714-24738  _maybe_hype_clip
  4008-4031   _migrate_columns
 23313-23324  _mod_is_exempt
 23327-23332  _mod_warn_first
 23335-23338  _mod_warn_text
 12377-12385  _modlog
   999-1001   _multistream_targets
  7472-7473   _nc_create_subprocess_exec
  7476-7477   _nc_create_subprocess_shell
 11117-11134  _news_loop
 12404-12406  _normalize_ingest
  2469-2486   _note_check_duration
  8409-8412   _notify_topic_name
 16252-16260  _oracle_memories
 16525-16559  _oracle_memorize
 16263-16276  _oracle_persona
 16245-16249  _oracle_recent_text
 12738-12746  _ov_atomic_write
 12726-12732  _ov_bar
 15104-15116  _ov_clip_text
 12735-12736  _ov_oneline
 18852-18881  _overlay_push
 13077-13120  _overlay_render_size
 12470-12474  _overlay_session_reset
 18816-18819  _overlay_src_ok
 15188-15198  _own_invites
 13072-13074  _parse_size
 19361-19441  _parse_ssh_attacks
  6895-6928   _pause_resume_cmd
  1865-1909   _persist_refreshed_cookies
  1768-1800   _pick_checked_pull_proxy
  9702-9715   _pin_auth_value
  9761-9762   _pin_clear_fail
  9741-9744   _pin_locked
  9747-9758   _pin_note_fail
  9718-9738   _pin_ok
 18710-18735  _piper_pick_model
 18747-18794  _piper_say
 11996-12031  _post_json_threaded
 13051-13069  _probe_video_size
  1651-1668   _proc_is_recorder
 10559-10587  _proxy_pool_refresh_loop
  1734-1765   _proxy_report_recording
 11651-11653  _prune_stall_dumps
 10936-11057  _public_stats
  1936-1942   _pull_proxy_still
 16788-16814  _push_notify
  9863-9865   _pwa_dir
 10316-10331  _quick_validate_proxy
 12062-12064  _quiet_hours_config
  9828-9861   _rate_guard
 16071-16077  _react_warn
  7380-7419   _reap_proc
  2509-2531   _record_check_outcome
   751-753    _redact_stream_urls
 10486-10556  _refresh_proxy_pool
  2302-2392   _resolve_via_html
  2651-2805   _resolve_via_webcast_api_v2
  2868-2930   _resolve_via_ytdlp
 22661-22790  _resolve_youtube_ingest
 12453-12464  _restream_active_sources
 17297-17396  _restream_chat_guardian
 12615-12687  _restream_chat_push
 12712-12721  _restream_chat_push_async
 13152-13239  _restream_html_overlay_start
 13242-13255  _restream_html_overlay_stop
 12415-12438  _restream_overlay_files
 17684-17716  _restream_platform_state
 17841-17876  _restream_resume_after_restart
 13303-13361  _restream_tts_enqueue_wav
 13013-13045  _restream_tts_feeder
 13010-13011  _restream_tts_fifo_path
 13258-13285  _restream_tts_start
 13287-13301  _restream_tts_stop
 17722-17838  _restream_verify_loop
 21649-21661  _retention_loop
 21643-21646  _retention_scan
  2613-2615   _room_is_abo
  5710-5827   _run_ai_call
 11789-11802  _run_async_from_flask
 19180-19183  _run_priv
 25442-25450  _run_selfcheck_and_exit
 21664-21675  _s3_client
  7629-7680   _safe_send
  4685-4701   _sample_net_throughput
  2561-2588   _schedule_next_check
 21597-21640  _scheduler_loop
  4034-4038   _schema_pk
 11806-11811  _scraper_session
 23341-23380  _screen_full
 11255-11292  _sec_headers
  2281-2283   _select_stream_from_data_section
 25255-25439  _selfcheck
  8421-8455   _send_live_notice
  1275-1279   _should_defer_upload
 22083-22118  _shrink_for_discord
  9868-9880   _sicheres_ziel
 21495-21515  _sicherheits_erinnerung_loop
 24635-24652  _sign_health_check
 24655-24674  _sign_health_loop
  7489-7500   _spawn
 25820-25850  _spawn_from_flask
 17022-17263  _start_chat_listener
 11769-11786  _start_loop_watchdog
 11084-11112  _stats_loop
 11063-11066  _stats_output_path
 11069-11081  _stats_write
  8149-8165   _storage_cleanup_loop
 24694-24701  _story_for
  3320-3326   _stream_url_expiry
  3335-3341   _stream_url_is_fresh
  3328-3333   _stream_url_ttl
 15151-15158  _streamer_persona_get
 12962-12966  _studio_chain
 21781-21903  _system_backup
 21912-21942  _system_backup_loop
 10268-10307  _test_proxy
 10814-10830  _testpush_resolve_live
  7605-7626   _tg_sprache_setzen
  8328-8338   _tg_topics_load_into_mem
  8325-8326   _tg_topics_path
  8340-8347   _tg_topics_save
  9676-9684   _token_ok
  8350-8354   _topic_forget
 12082-12093  _tracking_max_duration
  4298-4312   _tracking_remove_cleanup
  4329-4341   _tracking_resume_cleanup
  1517-1540   _try_attach_file_handler
 18737-18745  _tts_cleanup
 10790-10794  _tunnel_effective
 18233-18286  _twitch_channel_status
 23383-23528  _twitch_chat_loop
 23197-23300  _twitch_eventsub_loop
  1298-1311   _upload_queue_add
  1322-1324   _upload_queue_count
  1281-1290   _upload_queue_load
  1271-1273   _upload_queue_path
  1313-1320   _upload_queue_remove
  1292-1296   _upload_queue_save
  1326-1367   _upload_window_loop
  7353-7360   _uptime_s
 12392-12401  _url_host
   816-820    _usage_record_claude
  7543-7587   _verbindung_verloren
  6443-6474   _viewer_sample_loop
  9765-9768   _wants_html
  7363-7377   _warn_empty_env
 24428-24549  _watchdog_loop
 22936-22944  _wchat_thank_ok
 16856-16886  _whisper_get_model
  7450-7457   _whisper_native_section
 16058-16064  _whisper_pool
 16955-16984  _whisper_segments
 16888-16952  _whisper_transcribe
 12793-12955  _write_restream_overlay
 12755-12790  _write_restream_overlay_async
 23552-23632  _youtube_api_chat_loop
 18289-18392  _youtube_api_status
 18395-18462  _youtube_channel_status
 23635-23796  _youtube_chat_loop
 22796-22809  _youtube_restream_autoconfig
 22812-22836  _youtube_restream_autoconfig_inner
 22903-22931  _youtube_send
 18530-18571  _youtube_set_channel
 22839-22873  _yt_access_token
 22876-22891  _yt_live_chat_id
 22899-22900  _yt_sendrate_cfg
 23531-23546  _yt_timeout
  2852-2853   _ytdlp_detect_available
  2855-2866   _ytdlp_note_result
 11656-11658  _zombie_child_count
  7229-7253   about
  4209-4213   add_ai_log_entry
  4126-4129   add_archive_entry
  4723-4725   add_archive_rule
  4500-4534   add_recording
  4273-4290   add_tracking
  5830-5863   ai
  3861-3912   ai_chat
  3946-3956   ai_history_append
  3958-3963   ai_history_clear
  3935-3944   ai_history_load
  3920-3933   ai_rate_limit_check
  5892-5900   aireset
 16393-16412  azrael_chat
 23801-23923  brain_cmd
  3344-3528   build_recording_cmd
  4293-4296   bulk_add_trackings
  6697-6756   bulkadd
  8168-8308   check_all_trackings
  4345-4357   claim_live_transition
 15228-15990  class KickModerator
 13574-14991  class RestreamManager
 10673-10715  classify_proxy_anonymity
  5938-6136   cleanup
  4977-4983   cleanup_old_recordings
  4491-4498   clear_recording
 22553-22618  clip_moment
  4675-4678   compute_storage_forecast
  6819-6892   cookies_cmd
  4264-4270   count_trackings_for_chat
  4196-4207   decide_preferred_recorder
  4136-4139   delete_archive_entry
  4727-4729   delete_archive_rule
  5367-5514   diag
 24035-24096  einnahmen_cmd
  4669-4672   find_recordings_by_fingerprint
  4157-4173   finish_recording_attempt
  4317-4319   get_all_active_trackings
  4224-4226   get_all_checks
  4536-4539   get_all_recordings
  4618-4620   get_all_tags_with_counts
  4646-4649   get_annotations_for_recording
  4131-4134   get_archive_entry
  4639-4642   get_bookmarked_recordings
  2000-2146   get_cookie_health
  4606-4612   get_event_log
  4180-4194   get_last_recording_attempt
  2933-3038   get_live_status
  4916-4919   get_manual_recordings
  4654-4657   get_or_compute_inspect_sync
  5018-5021   get_outcome_breakdown
  4625-4628   get_priority_poll_interval
  4175-4178   get_recent_recording_attempts
  4541-4544   get_recording_by_id
  4632-4635   get_recording_note
  3662-3685   get_redis
  4253-4256   get_stats
  4971-4975   get_storage_stats
  4747-4749   get_tiktok_status_distribution
  4359-4368   get_tracking_state
  4314-4315   get_trackings_for_group
  4932-4935   get_trash_recordings
  8843-9511   handle_recording_finished
  4056-4081   init_db
  4719-4721   list_archive_rules
  5171-5209   live
  7683-7691   live_check_worker
  3740-3774   llm_chat
  3797-3825   llm_chat_sync
  3782-3794   llm_list_models
  4565-4598   log_event
  1585-1618   log_recording_failure
  7042-7091   logs_cmd
 24742-25245  main
  5866-5889   on_ai_media
  7168-7194   on_ai_reply
  7197-7226   on_azrael_mention
  7258-7288   on_callback
 16418-16522  oracle_handle
  6931-6934   pause_tracking
  5031-5036   profile_keyboard
  6993-7039   quota
  8072-8146   reaper_loop
  4743-4745   record_tiktok_status
  5905-5935   recstatus
  3687-3695   redis_get_json
  3698-3704   redis_set_json
 24099-24109  report_cmd
 10718-10720  report_proxy_result
  2395-2422   resolve_tiktok_live_stream
  4927-4930   restore_recording
  6937-6940   resume_tracking
  4732-4737   run_archive_rules
 24112-24335  run_bot
 11571-11623  run_flask
  4707-4710   sample_bandwidth_for_active
  4216-4222   save_tiktok_check
  4483-4489   set_recording_file
  4322-4326   set_tracking_paused
  4922-4925   soft_delete_recording
  8461-8841   split_and_send_video
  5084-5126   start
  4141-4155   start_recording_attempt
  6139-6177   stats
  4897-4914   stop_manual_recording
  6943-6990   stoprec
  6367-6375   summary_cmd
  7094-7165   sysres
  5516-5660   teststream
  5128-5169   tiktok
  6759-6816   topusers
  5246-5303   track
  5211-5243   track_exact
  5317-5365   tracklist
  4781-4895   trigger_manual_recording
  4444-4481   try_acquire_recording_lock
  4938-4940   universal_search
  5305-5315   untrack
 23926-24032  update_cmd
  4664-4667   update_recording_fingerprint
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
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            geschuetzt, host, lage, nur_lokal, offen_im_netz
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
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
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls, url_ohne_zugang
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
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
twitchoauth.py         access_token, authorize_url, configure, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
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
