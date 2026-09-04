# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (42)

```
 10081  GET              /                                                dashboard
 12263  GET              /api/abo/status                                  api_abo_status
 12217  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10869  GET              /api/automation/status                           api_automation_status
 10891  POST             /api/automation/toggle                           api_automation_toggle
 19067  GET              /api/channel/categories                          api_channel_categories
 19073  POST             /api/channel/set                                 api_channel_set
 18920  GET              /api/channels/status                             api_channels_status
 18594  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18577  GET              /api/clips                                       api_clips
 18623  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18502  GET              /api/debug/threads                               api_debug_threads
 12228  GET              /api/events                                      api_events
 11695  GET              /api/events/stream                               api_events_stream
 11361  GET              /api/health                                      api_health
 18536  POST             /api/highlights/config                           api_highlights_config
 10015  POST             /api/login                                       dashboard_login_submit
 12556  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11610  GET              /api/notify/status                               api_notify_status
 11621  POST             /api/notify/test                                 api_notify_test
 12317  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12294  GET              /api/proxy/trend                                 api_proxy_trend
 19995  GET              /api/selftest                                    api_selftest
 11920  GET              /api/system                                      api_system
 12611  GET              /api/system/check_timing                         api_check_timing
 12703  GET              /api/system/config_drift                         api_config_drift
 11426  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11468  GET              /api/system/preflight                            api_system_preflight
 11594  GET              /api/system/preflight_history                    api_system_preflight_history
 11760  GET              /api/system/resilience                           api_system_resilience
 18643  GET              /api/tts/<fn>                                    api_tts_file
 19369  GET              /api/upload_window                               api_upload_window
 11893  GET              /archive/<int:eid>/download                      archive_download
 11950  GET              /download/<int:recording_id>                     download
 11850  GET              /health                                          health
 18471  GET              /healthz                                         healthz
 10006  GET              /login                                           dashboard_login_page
 10036  GET              /logout                                          dashboard_logout
 10043  GET              /manifest.webmanifest                            pwa_manifest
 19342  GET              /overlay                                         overlay_page
 10067  GET              /pwa-icon-<variant>.png                          pwa_icon
 10053  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (317)

```
   173  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   380  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   185  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   155  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   994  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   734  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   865  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   845  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   883  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   807  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   347  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   358  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   368  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   391  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   398  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   409  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   542  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   640  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1232  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1264  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   331  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   947  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   927  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1100  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1148  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1199  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1058  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   902  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   366  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   630  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   512  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   495  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   487  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   323  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   339  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   674  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   639  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   659  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   546  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    40  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    69  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   277  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   357  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   334  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   152  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   401  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   455  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   155  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   116  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   137  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    82  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   235  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   161  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   179  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   151  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    54  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   127  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    70  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   103  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   111  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    51  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   127  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   156  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   141  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    81  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   103  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   124  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    71  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   171  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    35  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   191  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   211  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   238  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   352  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   275  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   372  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   367  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   443  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   220  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   210  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   232  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    91  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   159  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   137  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    76  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   116  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   166  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   386  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   215  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   258  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   325  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   353  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   204  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   271  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   506  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    71  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   169  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   152  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   392  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   216  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   168  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   451  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   426  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   287  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   133  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   305  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   485  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   480  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   528  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   411  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   738  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   465  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   438  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   712  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   582  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   671  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   577  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   510  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   290  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   755  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   378  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   633  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   788  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   773  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   334  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   572  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   558  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   541  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   598  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   691  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   587  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   477  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   455  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   496  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   513  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   565  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   431  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   256  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   156  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   587  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   404  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   125  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   526  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   552  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   182  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   207  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   379  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   324  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
   414  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   439  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   331  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   361  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   117  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   264  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    79  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   289  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   221  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   245  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   176  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   141  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   201  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    47  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   197  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   347  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   167  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   228  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   443  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   472  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   392  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   405  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   501  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   378  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   253  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   298  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   322  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   309  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   155  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   267  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   125  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   359  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   414  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   243  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   112  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    91  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   123  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   104  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   115  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    67  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    91  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    45  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   454  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   420  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   479  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   459  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   442  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   435  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   229  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   296  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    42  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    82  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   113  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    97  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   122  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   143  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   155  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    80  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   104  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    58  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   190  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   373  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 20679  /ai                     
 21152  /ask                    
 20770  /assign_role            
 20816  /ban                    
 21484  /botstats               
 21408  /clearwarns             
 21448  /clip                   
 21433  /clipoftheweek          
 21275  /clips                  
 20731  /create_category        
 20700  /create_channel         
 20759  /create_group           
 20742  /create_role            
 20716  /create_voice           
 21052  /daily                  
 21182  /event                  
 21225  /events                 
 21321  /follow                 
 21305  /help                   
 20805  /kick                   
 21034  /leaderboard            
 21261  /livenow                
 21291  /post_test              
 21122  /profile                
 20840  /purge                  
 21020  /rank                   
 21248  /recstatus              
 20781  /remove_role            
 20693  /restream_status        
 20792  /set_channel_perms      
 20985  /setup_community        
 21003  /setup_targets          
 21347  /stats                  
 20605  /status                 
 21643  /streaminfo             
 21540  /sys_report             
 21516  /sys_unpause            
 20827  /timeout                
 21419  /topstreamers           
 20635  /track                  
 20619  /tracklist              
 21336  /unfollow               
 20668  /untrack                
 21369  /warn                   
 21393  /warnings               
```

## Discord-Events (4)

```
 22141  on_member_join
 22103  on_message
 21730  on_raw_reaction_add
 22176  on_ready
```

## Top-Level-Symbole in bot.py (481 Funktionen, 2 Klassen)

```
  2550-2551   _abo_key
  2571-2589   _abo_probe_dump
 19579-19589  _active_recorder_sync
 15631-15638  _ad_allowlist
 16772-16778  _agent_for
 19591-19609  _ai_calls_total_sync
 16781-16797  _ai_telemetry
 17286-17304  _alert
 22292-22342  _alert_monitor_loop
 22694-22756  _announce_loop
  3492-3495   _anthropic_key
  3502-3504   _anthropic_model
  9759-9762   _arg_int
  2542-2547   _as_dict
 17440-17462  _audio_tap_cmd
  9927-9938   _auth_cookie
  9894-9923   _auth_guard
  1713-1718   _auto_on
 18333-18351  _auto_restream_loop
 23835-23850  _azrael_broadcast_reply
 23735-23757  _azrael_chat_reply
 23718-23732  _azrael_chat_should_reply
 23763-23765  _azrael_gate_cfg
 16802-16816  _azrael_live_state
 19254-19268  _azrael_overlay_state
 17168-17222  _azrael_proactive_loop
 16620-16676  _azrael_reaction_to_chats
 23768-23775  _azrael_reply_all_chats
 23705-23715  _azrael_self_names
 23803-23832  _azrael_send_to
 16822-16843  _azrael_system
 22426-22429  _backup_active
 22507-22520  _backup_loop
 22254-22263  _brain_growth_loop
 10260-10287  _brain_growth_snapshot
  2478-2498   _brain_hint_delay
  6166-6194   _brain_notify
 11674-11691  _browser_push
  6210-6297   _build_daily_summary
  2981-3161   _build_native_cmd
 13817-14004  _build_restream_cmd
  3205-3238   _build_ytdlp_cmd
 19531-19538  _cached_probe
  4988-5015   _can_stop_tracking
  1893-1915   _capture_set_cookies
 12371-12374  _cfg_get
 12377-12379  _cfg_set
 19028-19063  _channel_set_all
 12975-12978  _chat_connected
 12981-12997  _chat_disconnected
  8245-8256   _chat_is_forum
 13017-13019  _chat_sanitize
 12960-12972  _chat_stat
 13000-13003  _chat_stats_snapshot
  3770-3781   _check_ai_alive_sync
  3784-3796   _check_ai_models_sync
 19540-19553  _check_redis_alive_sync
 19555-19575  _check_redis_version_sync
 10542-10585  _classify_pool_anonymity
 10588-10605  _classify_pool_anonymity_bg
   827-849    _claude_chat_sync_metered
  9788-9795   _client_ip
 22788-22815  _clip_prune
 22818-22828  _clip_recfile_for
 23369-23375  _clip_should_velocity
 22869-22951  _clip_to_discord
  3668-3677   _close_ai_session
 23881-23896  _cohost_broadcast
 23866-23867  _cohost_cfg
 23922-23934  _cohost_fire_highlight
 23870-23878  _cohost_gate
 23899-23919  _cohost_highlight
 23000-23062  _community_events_loop
 10190-10192  _conv_messages
  6569-6612   _cookie_alarm_loop
  1965-1969   _cookie_autorefresh_info
  1870-1874   _cookie_header
 11724-11756  _cpu_load_snapshot
  3990-4002   _create_index_safe
 19773-19879  _crowdsec_status
 19719-19770  _crowdsec_via_lapi
 19623-19641  _cscli_bin
 19650-19663  _cscli_path
  6459-6484   _daily_summary_loop
 19681-19698  _darf_journal_lesen
 22266-22289  _db_maintenance_loop
  6428-6456   _db_vacuum_loop
 15654-15678  _detect_foreign_ad
  1448-1459   _diag_path_owner
 17074-17118  _director_finalize
 17886-17893  _director_for
 17023-17071  _director_mark
 23263-23298  _disc_automod_check
 23239-23242  _disc_state_get
 23245-23252  _disc_state_set
 20255-20268  _discord_guild_filesize_bytes
 20462-20466  _discord_invite
 23200-23236  _discord_live_thread
 17225-17237  _discord_notify
 20361-20386  _discord_ops_alert
 23098-23196  _discord_post_user
 20522-22251  _discord_run_once
 20401-20459  _discord_start
 22759-22765  _discord_stop
 20276-20278  _discord_upload_limit_label
 20271-20273  _discord_upload_limit_mb
  6487-6564   _disk_alarm_loop
 25314-25363  _disk_autoclean
 25366-25379  _disk_guard_loop
 25306-25311  _disk_pct
 13410-13412  _drawtext_chain
 12049-12051  _dump_all_threads
 10468-10531  _enrich_proxies_with_geo
  2110-2154   _ensure_cookie_file_netscape
 20469-20519  _ensure_discord_invite
 22965-22997  _ensure_error_channel
  8304-8307   _ensure_notify_topic
 10712-10749  _ensure_proxy_ready
  8258-8285   _ensure_topic
   684-686    _env_int
   689-691    _env_int_range
 23065-23095  _error_channel_loop
 17270-17283  _event_webhook
 12790-12803  _evolution_loop
  5608-5642   _extract_file_payload
  2226-2228   _extract_urls_from_streamurl_node
 19666-19673  _f2b_sudo_hint
 17306-17308  _faster_whisper_available
 10369-10387  _fetch_proxy_list
 17720-17748  _fetch_tiktok_room_id
   760-763    _ff_cmd
 13576-13581  _find_chromium
  3198-3202   _find_external_recorder
  2231-2233   _find_stream_urls
 12422-12447  _fire_webhooks
  7349-7358   _fork_safe
   860-873    _freeai_chat_sync_metered
 19712-19716  _geo_lookup_ips
  3656-3665   _get_ai_session
  7182-7222   _get_live_info
  2768-2775   _get_resolve_semaphore
  7582-7959   _handle_single_tracking
 25132-25134  _hb
 25137-25154  _hb_while
 13031-13033  _highlight_cfg
 13036-13065  _highlight_observe
 13584-13602  _htmlov_screenshot_cmd
 17464-17474  _httpx_proxy
 12455-12467  _in_quiet_hours
 26205-26236  _install_fast_eventloop
  9654-9708   _install_fast_json
 12054-12070  _install_faulthandler
 18379-18388  _intel_ensure_schema
 18426-18461  _intel_index_loop
 18400-18410  _intel_index_one
 18391-18397  _intel_semantic
  4977-4986   _is_authorized
  7483-7489   _is_dead
  2216-2218   _is_hevc
 19701-19703  _is_private_ip
  1612-1619   _is_process_running
  6196-6207   _is_quiet_hours
  1249-1258   _is_upload_window
  9743-9756   _json_error_handler
  6422-6423   _kick_broadcaster_id
  6334-6376   _kick_follower_count
  6318-6321   _kick_slug
 11302-11333  _kick_user_token
  4039-4042   _kind_from_filename
 12484-12489  _latest_popularity
 18101-18134  _live_react_loop
 17897-18090  _live_react_worker
 16679-16690  _live_transcript_push
 18092-18099  _live_users
 17121-17165  _living_title_loop
  1791-1864   _load_cookies_dict
 22432-22504  _local_backup_scan
  9725-9739   _log_5xx
 14012-14024  _looks_like_codec_err
 14007-14009  _looks_like_source_expired
  7399-7429   _loop_fehler
 12074-12083  _loop_heartbeat
 25102-25129  _loop_lag_monitor
 12086-12154  _loop_watchdog_thread
 16559-16573  _loyalty_add
 16550-16556  _loyalty_get
 16576-16584  _loyalty_top
 12597-12599  _manual_donations_total
  4695-4714   _manual_status
  7491-7492   _mark_dead
 10988-11004  _marketing_loop
 23782-23800  _maybe_handle_command
 25465-25489  _maybe_hype_clip
  3957-3980   _migrate_columns
 24061-24072  _mod_is_exempt
 24075-24080  _mod_warn_first
 24083-24086  _mod_warn_text
 12830-12838  _modlog
  1000-1002   _multistream_targets
  7361-7362   _nc_create_subprocess_exec
  7365-7366   _nc_create_subprocess_shell
 11239-11256  _news_loop
 12857-12859  _normalize_ingest
  2409-2426   _note_check_duration
  8298-8301   _notify_topic_name
 16705-16713  _oracle_memories
 16978-17012  _oracle_memorize
 16716-16729  _oracle_persona
 16698-16702  _oracle_recent_text
 13191-13199  _ov_atomic_write
 13179-13185  _ov_bar
 15557-15569  _ov_clip_text
 13188-13189  _ov_oneline
 19306-19335  _overlay_push
 13530-13573  _overlay_render_size
 12923-12927  _overlay_session_reset
 19270-19273  _overlay_src_ok
 15641-15651  _own_invites
 13525-13527  _parse_size
 19887-19967  _parse_ssh_attacks
  6784-6817   _pause_resume_cmd
  1919-1963   _persist_refreshed_cookies
  1757-1789   _pick_checked_pull_proxy
  9824-9837   _pin_auth_value
  9883-9884   _pin_clear_fail
  9863-9866   _pin_locked
  9869-9880   _pin_note_fail
  9840-9860   _pin_ok
 19164-19189  _piper_pick_model
 19201-19248  _piper_say
 12384-12419  _post_json_threaded
 13504-13522  _probe_video_size
  1640-1657   _proc_is_recorder
 10681-10709  _proxy_pool_refresh_loop
  1723-1754   _proxy_report_recording
 12039-12041  _prune_stall_dumps
 11058-11179  _public_stats
 17241-17267  _push_notify
  9985-9987   _pwa_dir
 10438-10453  _quick_validate_proxy
 12450-12452  _quiet_hours_config
  9950-9983   _rate_guard
 16524-16530  _react_warn
  7269-7308   _reap_proc
  2449-2471   _record_check_outcome
   755-757    _redact_stream_urls
 10608-10678  _refresh_proxy_pool
  2242-2332   _resolve_via_html
  2591-2745   _resolve_via_webcast_api_v2
  2808-2870   _resolve_via_ytdlp
 23409-23538  _resolve_youtube_ingest
 12906-12917  _restream_active_sources
 17751-17850  _restream_chat_guardian
 13068-13140  _restream_chat_push
 13165-13174  _restream_chat_push_async
 13605-13692  _restream_html_overlay_start
 13695-13708  _restream_html_overlay_stop
 12868-12891  _restream_overlay_files
 18138-18170  _restream_platform_state
 18295-18330  _restream_resume_after_restart
 13756-13814  _restream_tts_enqueue_wav
 13466-13498  _restream_tts_feeder
 13463-13464  _restream_tts_fifo_path
 13711-13738  _restream_tts_start
 13740-13754  _restream_tts_stop
 18176-18292  _restream_verify_loop
 22397-22409  _retention_loop
 22391-22394  _retention_scan
  2553-2555   _room_is_abo
  5646-5763   _run_ai_call
 12177-12190  _run_async_from_flask
 19706-19709  _run_priv
 26193-26201  _run_selfcheck_and_exit
 22412-22423  _s3_client
  7518-7569   _safe_send
  4621-4637   _sample_net_throughput
  2501-2528   _schedule_next_check
 22345-22388  _scheduler_loop
  3983-3987   _schema_pk
 12194-12199  _scraper_session
 24089-24128  _screen_full
 11377-11414  _sec_headers
  2221-2223   _select_stream_from_data_section
 26006-26190  _selfcheck
  8310-8344   _send_live_notice
  1272-1276   _should_defer_upload
 22831-22866  _shrink_for_discord
  9990-10002  _sicheres_ziel
 25386-25403  _sign_health_check
 25406-25425  _sign_health_loop
  7378-7389   _spawn
 26465-26495  _spawn_from_flask
 19988-19991  _st_befund
 17476-17717  _start_chat_listener
 12157-12174  _start_loop_watchdog
 11206-11234  _stats_loop
 11185-11188  _stats_output_path
 11191-11203  _stats_write
  8038-8054   _storage_cleanup_loop
 25445-25452  _story_for
  3260-3266   _stream_url_expiry
  3275-3281   _stream_url_is_fresh
  3268-3273   _stream_url_ttl
 15604-15611  _streamer_persona_get
 13415-13419  _studio_chain
 22529-22651  _system_backup
 22660-22690  _system_backup_loop
 10390-10429  _test_proxy
 10936-10952  _testpush_resolve_live
  7494-7515   _tg_sprache_setzen
  8217-8227   _tg_topics_load_into_mem
  8214-8215   _tg_topics_path
  8229-8236   _tg_topics_save
  9798-9806   _token_ok
  8239-8243   _topic_forget
 12470-12481  _tracking_max_duration
  4247-4261   _tracking_remove_cleanup
  4278-4290   _tracking_resume_cleanup
  1506-1529   _try_attach_file_handler
 19191-19199  _tts_cleanup
 10912-10916  _tunnel_effective
 18687-18740  _twitch_channel_status
 24131-24276  _twitch_chat_loop
 23945-24048  _twitch_eventsub_loop
  1295-1308   _upload_queue_add
  1319-1321   _upload_queue_count
  1278-1287   _upload_queue_load
  1268-1270   _upload_queue_path
  1310-1317   _upload_queue_remove
  1289-1293   _upload_queue_save
  1323-1364   _upload_window_loop
  7242-7249   _uptime_s
 12845-12854  _url_host
   735-752    _url_ohne_zugang
   820-824    _usage_record_claude
  7432-7476   _verbindung_verloren
  6379-6410   _viewer_sample_loop
  9887-9890   _wants_html
  7252-7266   _warn_empty_env
 25175-25296  _watchdog_loop
 23684-23692  _wchat_thank_ok
 17310-17340  _whisper_get_model
  7339-7346   _whisper_native_section
 16511-16517  _whisper_pool
 17409-17438  _whisper_segments
 17342-17406  _whisper_transcribe
 13246-13408  _write_restream_overlay
 13208-13243  _write_restream_overlay_async
 24300-24380  _youtube_api_chat_loop
 18743-18846  _youtube_api_status
 18849-18916  _youtube_channel_status
 24383-24544  _youtube_chat_loop
 23544-23557  _youtube_restream_autoconfig
 23560-23584  _youtube_restream_autoconfig_inner
 23651-23679  _youtube_send
 18984-19025  _youtube_set_channel
 23587-23621  _yt_access_token
 23624-23639  _yt_live_chat_id
 23647-23648  _yt_sendrate_cfg
 24279-24294  _yt_timeout
  2792-2793   _ytdlp_detect_available
  2795-2806   _ytdlp_note_result
 12044-12046  _zombie_child_count
  7118-7142   about
  4158-4162   add_ai_log_entry
  4075-4078   add_archive_entry
  4659-4661   add_archive_rule
  4449-4483   add_recording
  4222-4239   add_tracking
  5766-5799   ai
  3810-3861   ai_chat
  3895-3905   ai_history_append
  3907-3912   ai_history_clear
  3884-3893   ai_history_load
  3869-3882   ai_rate_limit_check
  5828-5836   aireset
 16846-16865  azrael_chat
 24549-24671  brain_cmd
  3284-3468   build_recording_cmd
  4242-4245   bulk_add_trackings
  6615-6674   bulkadd
  8057-8197   check_all_trackings
  4294-4306   claim_live_transition
 15681-16443  class KickModerator
 14027-15444  class RestreamManager
 10795-10837  classify_proxy_anonymity
  5874-6072   cleanup
  4913-4919   cleanup_old_recordings
  4440-4447   clear_recording
 23301-23366  clip_moment
  4611-4614   compute_storage_forecast
  6737-6781   cookies_cmd
  4213-4219   count_trackings_for_chat
  4145-4156   decide_preferred_recorder
  4085-4088   delete_archive_entry
  4663-4665   delete_archive_rule
  5303-5450   diag
 24783-24844  einnahmen_cmd
  4605-4608   find_recordings_by_fingerprint
  4106-4122   finish_recording_attempt
  4266-4268   get_all_active_trackings
  4173-4175   get_all_checks
  4485-4488   get_all_recordings
  4554-4556   get_all_tags_with_counts
  4582-4585   get_annotations_for_recording
  4080-4083   get_archive_entry
  4575-4578   get_bookmarked_recordings
  1986-2103   get_cookie_health
  4542-4548   get_event_log
  4129-4143   get_last_recording_attempt
  2873-2978   get_live_status
  4852-4855   get_manual_recordings
  4590-4593   get_or_compute_inspect_sync
  4954-4957   get_outcome_breakdown
  4561-4564   get_priority_poll_interval
  4124-4127   get_recent_recording_attempts
  4490-4493   get_recording_by_id
  4568-4571   get_recording_note
  3602-3625   get_redis
  4202-4205   get_stats
  4907-4911   get_storage_stats
  4683-4685   get_tiktok_status_distribution
  4308-4317   get_tracking_state
  4263-4264   get_trackings_for_group
  4868-4871   get_trash_recordings
  8965-9633   handle_recording_finished
  4005-4030   init_db
  4655-4657   list_archive_rules
  5107-5145   live
  7572-7580   live_check_worker
  3680-3714   llm_chat
  3737-3765   llm_chat_sync
  3722-3734   llm_list_models
  4501-4534   log_event
  1574-1607   log_recording_failure
  6931-6980   logs_cmd
 25493-25996  main
  5802-5825   on_ai_media
  7057-7083   on_ai_reply
  7086-7115   on_azrael_mention
  7147-7177   on_callback
 16871-16975  oracle_handle
  6820-6823   pause_tracking
  4967-4972   profile_keyboard
  6882-6928   quota
  7961-8035   reaper_loop
  4679-4681   record_tiktok_status
  5841-5871   recstatus
  3627-3635   redis_get_json
  3638-3644   redis_set_json
 24847-24857  report_cmd
 10840-10842  report_proxy_result
  2335-2362   resolve_tiktok_live_stream
  4863-4866   restore_recording
  6826-6829   resume_tracking
  4668-4673   run_archive_rules
 24860-25082  run_bot
 11964-12011  run_flask
  4643-4646   sample_bandwidth_for_active
  4165-4171   save_tiktok_check
  4432-4438   set_recording_file
  4271-4275   set_tracking_paused
  4858-4861   soft_delete_recording
  8350-8963   split_and_send_video
  5020-5062   start
  4090-4104   start_recording_attempt
  6075-6113   stats
  4833-4850   stop_manual_recording
  6832-6879   stoprec
  6303-6311   summary_cmd
  6983-7054   sysres
  5452-5596   teststream
  5064-5105   tiktok
  6677-6734   topusers
  5182-5239   track
  5147-5179   track_exact
  5253-5301   tracklist
  4717-4831   trigger_manual_recording
  4393-4430   try_acquire_recording_lock
  4874-4876   universal_search
  5241-5251   untrack
 24674-24780  update_cmd
  4600-4603   update_recording_fingerprint
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
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_async, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
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
logsafe.py             redact_stream_urls
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
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
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
