# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (81)

```
 10349  GET              /                                                dashboard
 12855  GET              /api/abo/status                                  api_abo_status
 10422  GET              /api/active-recordings                           api_active_recordings
 12926  GET              /api/activity-pulse                              api_activity_pulse
 12754  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 12809  GET/POST         /api/auto-archive-rules                          api_archive_rules
 12833  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 12837  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11290  GET              /api/automation/status                           api_automation_status
 11312  POST             /api/automation/toggle                           api_automation_toggle
 12314  POST             /api/backup/run                                  api_backup_run
 12280  GET              /api/backup/status                               api_backup_status
 12269  POST             /api/backup/system                               api_backup_system
 12786  GET              /api/bandwidth/live                              api_bandwidth_live
 12739  GET              /api/bookmarks                                   api_bookmarks_list
 19636  GET              /api/channel/categories                          api_channel_categories
 19642  POST             /api/channel/set                                 api_channel_set
 19489  GET              /api/channels/status                             api_channels_status
 10403  GET              /api/checks                                      api_checks
 19163  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19146  GET              /api/clips                                       api_clips
 19192  POST/DELETE      /api/clips/clear                                 api_clips_clear
 13198  GET              /api/community/stats                             api_community_stats
 20073  GET              /api/data/export                                 api_data_export
 19061  GET              /api/debug/threads                               api_debug_threads
 20920  GET              /api/defense/attacks                             api_defense_attacks
 20887  GET              /api/defense/crowdsec                            api_defense_crowdsec
 20905  GET              /api/defense/fail2ban                            api_defense_fail2ban
 20611  GET              /api/defense/overview                            api_defense_overview
 12768  GET              /api/events                                      api_events
 12151  GET              /api/events/stream                               api_events_stream
 12781  GET              /api/forecast/storage                            api_forecast_storage
 11328  GET              /api/freeai/status                               api_freeai_status
 11800  GET              /api/health                                      api_health
 12799  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 12795  GET              /api/heatmap/recordings                          api_heatmap_recordings
 19093  GET              /api/highlights                                  api_highlights
 19105  POST             /api/highlights/config                           api_highlights_config
 10283  POST             /api/login                                       dashboard_login_submit
 13183  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 13152  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12049  GET              /api/notify/status                               api_notify_status
 12060  POST             /api/notify/test                                 api_notify_test
 10507  GET              /api/outcomes                                    api_outcomes
 12909  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12886  GET              /api/proxy/trend                                 api_proxy_trend
 11666  GET              /api/public/stats                                api_public_stats
 10383  GET              /api/pulse                                       api_pulse
 12373  GET              /api/recording-attempts                          api_recording_attempts
 12098  GET              /api/retention/preview                           api_retention_preview
 12107  POST             /api/retention/run                               api_retention_run
 12724  GET              /api/search                                      api_search
 20658  GET              /api/selftest                                    api_selftest
 18899  GET              /api/shield/stats                                api_shield_stats
 10444  GET              /api/storage                                     api_storage
 10451  POST             /api/storage/cleanup                             api_storage_cleanup
 10475  GET              /api/summary/preview                             api_summary_preview
 12438  GET              /api/system                                      api_system
 13231  GET              /api/system/check_timing                         api_check_timing
 13323  GET              /api/system/config_drift                         api_config_drift
 11865  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11907  GET              /api/system/preflight                            api_system_preflight
 12033  GET              /api/system/preflight_history                    api_system_preflight_history
 12216  GET              /api/system/resilience                           api_system_resilience
 12759  GET              /api/tags                                        api_tags_list
 10417  GET              /api/top                                         api_top
 10617  GET              /api/trend-7d                                    api_trend_7d
 19212  GET              /api/tts/<fn>                                    api_tts_file
 19938  GET              /api/upload_window                               api_upload_window
 10521  GET              /api/userstats                                   api_userstats
 11714  GET              /api/version                                     api_version
 12411  GET              /archive/<int:eid>/download                      archive_download
 12468  GET              /download/<int:recording_id>                     download
 12351  GET              /health                                          health
 19030  GET              /healthz                                         healthz
 10274  GET              /login                                           dashboard_login_page
 10304  GET              /logout                                          dashboard_logout
 10311  GET              /manifest.webmanifest                            pwa_manifest
 19911  GET              /overlay                                         overlay_page
 10335  GET              /pwa-icon-<variant>.png                          pwa_icon
 10321  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (278)

```
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
   272  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   211  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   163  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   446  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   421  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
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
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   434  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   326  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   356  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
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
   368  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 21384  /ai                     
 21843  /ask                    
 21475  /assign_role            
 21521  /ban                    
 22175  /botstats               
 22099  /clearwarns             
 22139  /clip                   
 22124  /clipoftheweek          
 21966  /clips                  
 21436  /create_category        
 21405  /create_channel         
 21464  /create_group           
 21447  /create_role            
 21421  /create_voice           
 21757  /daily                  
 21873  /event                  
 21916  /events                 
 22012  /follow                 
 21996  /help                   
 21510  /kick                   
 21739  /leaderboard            
 21952  /livenow                
 21982  /post_test              
 21813  /profile                
 21545  /purge                  
 21725  /rank                   
 21939  /recstatus              
 21486  /remove_role            
 21398  /restream_status        
 21497  /set_channel_perms      
 21690  /setup_community        
 21708  /setup_targets          
 22038  /stats                  
 21310  /status                 
 22334  /streaminfo             
 22231  /sys_report             
 22207  /sys_unpause            
 21532  /timeout                
 22110  /topstreamers           
 21340  /track                  
 21324  /tracklist              
 22027  /unfollow               
 21373  /untrack                
 22060  /warn                   
 22084  /warnings               
```

## Discord-Events (4)

```
 22820  on_member_join
 22782  on_message
 22421  on_raw_reaction_add
 22855  on_ready
```

## Top-Level-Symbole in bot.py (479 Funktionen, 2 Klassen)

```
  2509-2510   _abo_key
  2530-2548   _abo_probe_dump
 20180-20190  _active_recorder_sync
 16164-16171  _ad_allowlist
 17305-17311  _agent_for
 20192-20210  _ai_calls_total_sync
 17314-17330  _ai_telemetry
 17819-17837  _alert
 22971-23021  _alert_monitor_loop
 23402-23464  _announce_loop
  3451-3454   _anthropic_key
  3461-3463   _anthropic_model
 10027-10030  _arg_int
  2501-2506   _as_dict
 17973-17995  _audio_tap_cmd
 10195-10206  _auth_cookie
 10162-10191  _auth_guard
  1672-1677   _auto_on
 18865-18883  _auto_restream_loop
 24515-24530  _azrael_broadcast_reply
 24415-24437  _azrael_chat_reply
 24398-24412  _azrael_chat_should_reply
 24443-24445  _azrael_gate_cfg
 17335-17349  _azrael_live_state
 19823-19837  _azrael_overlay_state
 17701-17755  _azrael_proactive_loop
 17153-17209  _azrael_reaction_to_chats
 24448-24455  _azrael_reply_all_chats
 24385-24395  _azrael_self_names
 24483-24512  _azrael_send_to
 17355-17376  _azrael_system
 23140-23143  _backup_active
 23221-23234  _backup_loop
 22933-22942  _brain_growth_loop
 10668-10695  _brain_growth_snapshot
  2437-2457   _brain_hint_delay
  6460-6488   _brain_notify
 12130-12147  _browser_push
  6504-6591   _build_daily_summary
  2940-3120   _build_native_cmd
 14352-14539  _build_restream_cmd
  3164-3197   _build_ytdlp_cmd
 20132-20139  _cached_probe
  5282-5309   _can_stop_tracking
  1852-1874   _capture_set_cookies
 12967-12970  _cfg_get
 12973-12975  _cfg_set
 19597-19632  _channel_set_all
 13595-13598  _chat_connected
 13601-13617  _chat_disconnected
  8518-8529   _chat_is_forum
 13637-13639  _chat_sanitize
 13580-13592  _chat_stat
 13620-13623  _chat_stats_snapshot
  3729-3740   _check_ai_alive_sync
  3743-3755   _check_ai_models_sync
 20141-20154  _check_redis_alive_sync
 20156-20176  _check_redis_version_sync
 10963-11006  _classify_pool_anonymity
 11009-11026  _classify_pool_anonymity_bg
   823-827    _claude_chat_sync_metered
 10056-10063  _client_ip
 23496-23523  _clip_prune
 23526-23536  _clip_recfile_for
 24049-24055  _clip_should_velocity
 23577-23659  _clip_to_discord
  3627-3636   _close_ai_session
 24561-24576  _cohost_broadcast
 24546-24547  _cohost_cfg
 24602-24614  _cohost_fire_highlight
 24550-24558  _cohost_gate
 24579-24599  _cohost_highlight
 23708-23742  _community_events_loop
 10568-10570  _conv_messages
  6860-6903   _cookie_alarm_loop
  1924-1928   _cookie_autorefresh_info
  1829-1833   _cookie_header
 12180-12212  _cpu_load_snapshot
  3949-3961   _create_index_safe
 20413-20519  _crowdsec_status
 20359-20410  _crowdsec_via_lapi
 20224-20242  _cscli_bin
 20248-20261  _cscli_path
  6750-6775   _daily_summary_loop
 20279-20296  _darf_journal_lesen
 22945-22968  _db_maintenance_loop
  6719-6747   _db_vacuum_loop
 16187-16211  _detect_foreign_ad
  1410-1421   _diag_path_owner
 17607-17651  _director_finalize
 18419-18426  _director_for
 17556-17604  _director_mark
 23943-23978  _disc_automod_check
 23919-23922  _disc_state_get
 23925-23932  _disc_state_set
 20962-20975  _discord_guild_filesize_bytes
 21167-21171  _discord_invite
 23880-23916  _discord_live_thread
 17758-17770  _discord_notify
 21066-21091  _discord_ops_alert
 23778-23876  _discord_post_user
 21227-22930  _discord_run_once
 21106-21164  _discord_start
 23467-23473  _discord_stop
 20983-20985  _discord_upload_limit_label
 20978-20980  _discord_upload_limit_mb
  6778-6855   _disk_alarm_loop
 25994-26043  _disk_autoclean
 26046-26059  _disk_guard_loop
 25986-25991  _disk_pct
 13945-13947  _drawtext_chain
 12567-12569  _dump_all_threads
 10888-10952  _enrich_proxies_with_geo
  2069-2113   _ensure_cookie_file_netscape
 21174-21224  _ensure_discord_invite
 23673-23705  _ensure_error_channel
  8577-8580   _ensure_notify_topic
 11133-11170  _ensure_proxy_ready
  8531-8558   _ensure_topic
   680-682    _env_int
   685-687    _env_int_range
 23745-23775  _error_channel_loop
 17803-17816  _event_webhook
 13410-13423  _evolution_loop
  5902-5936   _extract_file_payload
  2185-2187   _extract_urls_from_streamurl_node
 20264-20271  _f2b_sudo_hint
 17839-17841  _faster_whisper_available
 10777-10795  _fetch_proxy_list
 18253-18281  _fetch_tiktok_room_id
   756-759    _ff_cmd
 14111-14116  _find_chromium
  3157-3161   _find_external_recorder
  2190-2192   _find_stream_urls
 13018-13043  _fire_webhooks
  7640-7649   _fork_safe
   838-847    _freeai_chat_sync_metered
 20314-20356  _geo_lookup_ips
  3615-3624   _get_ai_session
  7473-7513   _get_live_info
  2727-2734   _get_resolve_semaphore
  7873-8239   _handle_single_tracking
 25812-25814  _hb
 25817-25834  _hb_while
 13646-13648  _highlight_cfg
 13651-13680  _highlight_observe
 14119-14137  _htmlov_screenshot_cmd
 17997-18007  _httpx_proxy
 13051-13063  _in_quiet_hours
 26885-26916  _install_fast_eventloop
  9922-9976   _install_fast_json
 12572-12588  _install_faulthandler
 18938-18947  _intel_ensure_schema
 18985-19020  _intel_index_loop
 18959-18969  _intel_index_one
 18950-18956  _intel_semantic
  5271-5280   _is_authorized
  7774-7780   _is_dead
  2175-2177   _is_hevc
 20299-20305  _is_private_ip
  1574-1581   _is_process_running
  6490-6501   _is_quiet_hours
  1211-1220   _is_upload_window
 10011-10024  _json_error_handler
  6713-6714   _kick_broadcaster_id
  6625-6667   _kick_follower_count
  6609-6612   _kick_slug
 11741-11772  _kick_user_token
  3998-4001   _kind_from_filename
 13080-13085  _latest_popularity
 18634-18667  _live_react_loop
 18430-18623  _live_react_worker
 17212-17223  _live_transcript_push
 18625-18632  _live_users
 17654-17698  _living_title_loop
  1750-1823   _load_cookies_dict
 23146-23218  _local_backup_scan
  9993-10007  _log_5xx
 14547-14559  _looks_like_codec_err
 14542-14544  _looks_like_source_expired
  7690-7720   _loop_fehler
 12592-12601  _loop_heartbeat
 25782-25809  _loop_lag_monitor
 12604-12672  _loop_watchdog_thread
 17092-17106  _loyalty_add
 17083-17089  _loyalty_get
 17109-17117  _loyalty_top
 13217-13219  _manual_donations_total
  7782-7783   _mark_dead
 11419-11435  _marketing_loop
 24462-24480  _maybe_handle_command
 26145-26169  _maybe_hype_clip
  3916-3939   _migrate_columns
 24741-24752  _mod_is_exempt
 24755-24760  _mod_warn_first
 24763-24766  _mod_warn_text
 13450-13458  _modlog
   962-964    _multistream_targets
  7652-7653   _nc_create_subprocess_exec
  7656-7657   _nc_create_subprocess_shell
 11671-11688  _news_loop
 13477-13479  _normalize_ingest
  2368-2385   _note_check_duration
  8571-8574   _notify_topic_name
 17238-17246  _oracle_memories
 17511-17545  _oracle_memorize
 17249-17262  _oracle_persona
 17231-17235  _oracle_recent_text
 13771-13779  _ov_atomic_write
 13759-13765  _ov_bar
 16090-16102  _ov_clip_text
 13768-13769  _ov_oneline
 19875-19904  _overlay_push
 14065-14108  _overlay_render_size
 13543-13547  _overlay_session_reset
 19839-19842  _overlay_src_ok
 16174-16184  _own_invites
 14060-14062  _parse_size
 20527-20607  _parse_ssh_attacks
  7075-7108   _pause_resume_cmd
  1878-1922   _persist_refreshed_cookies
  1716-1748   _pick_checked_pull_proxy
 10092-10105  _pin_auth_value
 10151-10152  _pin_clear_fail
 10131-10134  _pin_locked
 10137-10148  _pin_note_fail
 10108-10128  _pin_ok
 19733-19758  _piper_pick_model
 19770-19817  _piper_say
 12980-13015  _post_json_threaded
 14039-14057  _probe_video_size
  1602-1619   _proc_is_recorder
 10875-10886  _proxy_geo_cache_put
 11102-11130  _proxy_pool_refresh_loop
  1682-1713   _proxy_report_recording
 12557-12559  _prune_stall_dumps
 11489-11610  _public_stats
 17774-17800  _push_notify
 10253-10255  _pwa_dir
 10846-10861  _quick_validate_proxy
 13046-13048  _quiet_hours_config
 10218-10251  _rate_guard
 17057-17063  _react_warn
  7560-7599   _reap_proc
  2408-2430   _record_check_outcome
   751-753    _redact_stream_urls
 11029-11099  _refresh_proxy_pool
  2201-2291   _resolve_via_html
  2550-2704   _resolve_via_webcast_api_v2
  2767-2829   _resolve_via_ytdlp
 24089-24218  _resolve_youtube_ingest
 13526-13537  _restream_active_sources
 18284-18383  _restream_chat_guardian
 13683-13755  _restream_chat_push
 14140-14227  _restream_html_overlay_start
 14230-14243  _restream_html_overlay_stop
 13488-13511  _restream_overlay_files
 18671-18703  _restream_platform_state
 18827-18862  _restream_resume_after_restart
 14291-14349  _restream_tts_enqueue_wav
 14001-14033  _restream_tts_feeder
 13998-13999  _restream_tts_fifo_path
 14246-14273  _restream_tts_start
 14275-14289  _restream_tts_stop
 18709-18824  _restream_verify_loop
 23111-23123  _retention_loop
 23070-23108  _retention_scan
  2512-2514   _room_is_abo
  5940-6057   _run_ai_call
 12695-12708  _run_async_from_flask
 20308-20311  _run_priv
 26873-26881  _run_selfcheck_and_exit
 23126-23137  _s3_client
  7809-7860   _safe_send
  4620-4636   _sample_net_throughput
  2460-2487   _schedule_next_check
 23024-23067  _scheduler_loop
  3942-3946   _schema_pk
 12712-12717  _scraper_session
 24769-24808  _screen_full
 11816-11853  _sec_headers
  2180-2182   _select_stream_from_data_section
 26686-26870  _selfcheck
  8583-8617   _send_live_notice
  1234-1238   _should_defer_upload
 23539-23574  _shrink_for_discord
 10258-10270  _sicheres_ziel
 26066-26083  _sign_health_check
 26086-26105  _sign_health_loop
  7669-7680   _spawn
 27145-27175  _spawn_from_flask
 20651-20654  _st_befund
 18009-18250  _start_chat_listener
 12675-12692  _start_loop_watchdog
 11634-11662  _stats_loop
 11613-11616  _stats_output_path
 11619-11631  _stats_write
  8311-8327   _storage_cleanup_loop
 26125-26132  _story_for
  3219-3225   _stream_url_expiry
  3234-3240   _stream_url_is_fresh
  3227-3232   _stream_url_ttl
 16137-16144  _streamer_persona_get
 13950-13954  _studio_chain
 23243-23365  _system_backup
 23368-23398  _system_backup_loop
 10798-10837  _test_proxy
 11367-11383  _testpush_resolve_live
  7785-7806   _tg_sprache_setzen
  8490-8500   _tg_topics_load_into_mem
  8487-8488   _tg_topics_path
  8502-8509   _tg_topics_save
 10066-10074  _token_ok
  8512-8516   _topic_forget
 13066-13077  _tracking_max_duration
  4207-4221   _tracking_remove_cleanup
  4238-4250   _tracking_resume_cleanup
  1468-1491   _try_attach_file_handler
 19760-19768  _tts_cleanup
 11343-11347  _tunnel_effective
 19256-19309  _twitch_channel_status
 24811-24956  _twitch_chat_loop
 24625-24728  _twitch_eventsub_loop
  1257-1270   _upload_queue_add
  1281-1283   _upload_queue_count
  1240-1249   _upload_queue_load
  1230-1232   _upload_queue_path
  1272-1279   _upload_queue_remove
  1251-1255   _upload_queue_save
  1285-1326   _upload_window_loop
  7533-7540   _uptime_s
 13465-13474  _url_host
   731-748    _url_ohne_zugang
   816-820    _usage_record_claude
  7723-7767   _verbindung_verloren
  6670-6701   _viewer_sample_loop
 10155-10158  _wants_html
  7543-7557   _warn_empty_env
 25855-25976  _watchdog_loop
 24364-24372  _wchat_thank_ok
 17843-17873  _whisper_get_model
  7630-7637   _whisper_native_section
 17044-17050  _whisper_pool
 17942-17971  _whisper_segments
 17875-17939  _whisper_transcribe
 13781-13943  _write_restream_overlay
 24980-25060  _youtube_api_chat_loop
 19312-19415  _youtube_api_status
 19418-19485  _youtube_channel_status
 25063-25224  _youtube_chat_loop
 24224-24237  _youtube_restream_autoconfig
 24240-24264  _youtube_restream_autoconfig_inner
 24331-24359  _youtube_send
 19553-19594  _youtube_set_channel
 24267-24301  _yt_access_token
 24304-24319  _yt_live_chat_id
 24327-24328  _yt_sendrate_cfg
 24959-24974  _yt_timeout
  2751-2752   _ytdlp_detect_available
  2754-2765   _ytdlp_note_result
 12562-12564  _zombie_child_count
  7409-7433   about
  4117-4121   add_ai_log_entry
  4034-4037   add_archive_entry
  4703-4718   add_archive_rule
  4409-4443   add_recording
  4182-4199   add_tracking
  6060-6093   ai
  3769-3820   ai_chat
  3854-3864   ai_history_append
  3866-3871   ai_history_clear
  3843-3852   ai_history_load
  3828-3841   ai_rate_limit_check
  6122-6130   aireset
 17379-17398  azrael_chat
 25229-25351  brain_cmd
  3243-3427   build_recording_cmd
  4202-4205   bulk_add_trackings
  6906-6965   bulkadd
  8330-8470   check_all_trackings
  4254-4266   claim_live_transition
 16214-16976  class KickModerator
 14562-15977  class RestreamManager
 11216-11258  classify_proxy_anonymity
  6168-6366   cleanup
  5131-5172   cleanup_old_recordings
  4400-4407   clear_recording
 23981-24046  clip_moment
  4564-4613   compute_storage_forecast
  7028-7072   cookies_cmd
  4173-4179   count_trackings_for_chat
  4104-4115   decide_preferred_recorder
  4044-4047   delete_archive_entry
  4720-4728   delete_archive_rule
  5597-5744   diag
 25463-25524  einnahmen_cmd
  4558-4561   find_recordings_by_fingerprint
  4065-4081   finish_recording_attempt
  4226-4228   get_all_active_trackings
  4132-4135   get_all_checks
  4445-4448   get_all_recordings
  4507-4509   get_all_tags_with_counts
  4535-4538   get_annotations_for_recording
  4039-4042   get_archive_entry
  4528-4531   get_bookmarked_recordings
  1945-2062   get_cookie_health
  4495-4501   get_event_log
  4088-4102   get_last_recording_attempt
  2832-2937   get_live_status
  4986-4989   get_manual_recordings
  4543-4546   get_or_compute_inspect_sync
  5207-5251   get_outcome_breakdown
  4514-4517   get_priority_poll_interval
  4083-4086   get_recent_recording_attempts
  4450-4453   get_recording_by_id
  4521-4524   get_recording_note
  3561-3584   get_redis
  4162-4165   get_stats
  5098-5129   get_storage_stats
  4821-4823   get_tiktok_status_distribution
  4268-4277   get_tracking_state
  4223-4224   get_trackings_for_group
  5002-5005   get_trash_recordings
  9238-9901   handle_recording_finished
  3964-3989   init_db
  4693-4701   list_archive_rules
  5401-5439   live
  7863-7871   live_check_worker
  3639-3673   llm_chat
  3696-3724   llm_chat_sync
  3681-3693   llm_list_models
  4461-4487   log_event
  1536-1569   log_recording_failure
  7222-7271   logs_cmd
 26173-26676  main
  6096-6119   on_ai_media
  7348-7374   on_ai_reply
  7377-7406   on_azrael_mention
  7438-7468   on_callback
 17404-17508  oracle_handle
  7111-7114   pause_tracking
  5261-5266   profile_keyboard
  7173-7219   quota
  8241-8308   reaper_loop
  4817-4819   record_tiktok_status
  6135-6165   recstatus
  3586-3594   redis_get_json
  3597-3603   redis_set_json
 25527-25537  report_cmd
 11261-11263  report_proxy_result
  2294-2321   resolve_tiktok_live_stream
  4997-5000   restore_recording
  7117-7120   resume_tracking
  4731-4811   run_archive_rules
 25540-25762  run_bot
 12482-12529  run_flask
  4639-4684   sample_bandwidth_for_active
  4124-4130   save_tiktok_check
  4392-4398   set_recording_file
  4231-4235   set_tracking_paused
  4992-4995   soft_delete_recording
  8623-9236   split_and_send_video
  5314-5356   start
  4049-4063   start_recording_attempt
  6369-6407   stats
  4967-4984   stop_manual_recording
  7123-7170   stoprec
  6594-6602   summary_cmd
  7274-7345   sysres
  5746-5890   teststream
  5358-5399   tiktok
  6968-7025   topusers
  5476-5533   track
  5441-5473   track_exact
  5547-5595   tracklist
  4833-4965   trigger_manual_recording
  4353-4390   try_acquire_recording_lock
  5008-5067   universal_search
  5535-5545   untrack
 25354-25460  update_cmd
  4553-4556   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
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
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
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
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
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
